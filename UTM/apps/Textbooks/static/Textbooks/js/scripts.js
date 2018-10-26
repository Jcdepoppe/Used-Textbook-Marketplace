$(document).ready(function () { // only begin once page has loaded
    $('#txtBookSearch').autocomplete({ // attach auto-complete functionality to textbox
        // define source of the data
        source: function (request, response) {
            // url link to google books, including text entered by user (request.term)
            var booksUrl = 'https://www.googleapis.com/books/v1/volumes?printType=books&q=' + encodeURIComponent(request.term);
            $.ajax({
                url: booksUrl,
                dataType: 'jsonp',
                success: function(data) {
                    response($.map(data.items, function (item) {
                        if (item.volumeInfo.authors && item.volumeInfo.title
                        && item.volumeInfo.industryIdentifiers && item.volumeInfo.publishedDate) {
                            return {
                                // label value will be shown in the suggestions
                                label: item.volumeInfo.title + ', ' + item.volumeInfo.authors[0] + ', ' + item.volumeInfo.publishedDate,
                                // value is what gets put in the textbox once an item selected
                                value: item.volumeInfo.title,
                                // other individual values to use later
                                title: item.volumeInfo.title,
                                author: item.volumeInfo.authors[0],
                                isbn: item.volumeInfo.industryIdentifiers,
                                publishedDate: item.volumeInfo.publishedDate,
                                image: (item.volumeInfo.imageLinks == null ? '' : item.volumeInfo.imageLinks.thumbnail),
                                publisher: item.volumeInfo.publisher
                            };
                        }
                    }));
                }
            });
        },
        select: function (event, ui) {
            // what to do when an item is selected
            // first clear anything that may already be in the description
            $('#divDescription').empty();
            // we get the currently selected item using ui.item
            // show a pic if we have one
            if (ui.item.image != '') {
                $('#divDescription').append('<img src="' + ui.item.image + '" style="float: left; padding: 10px;">');
            }
            // and title, author, and year
            $('#divDescription').append('<p><b>Title:</b> ' + ui.item.title  + '</p>');
            $('#divDescription').append('<p><b>Author:</b> ' + ui.item.author  + '</p>');
            $('#divDescription').append('<p><b>First published year:</b> ' + ui.item.publishedDate  + '</p>');
            $('#divDescription').append('<p><b>Publisher:</b> ' + ui.item.publisher  + '</p>');
            // and show the link to oclc (if we have an isbn number)
            if (ui.item.isbn && ui.item.isbn[0].identifier) {
                $('#divDescription').append('<p><b>ISBN:</b> '
                + ui.item.isbn[0].identifier + '</p>');
            }
            $('#bookInfo').empty();
            // The value only saves one 'word'(A string that removes everything after the first space it hits). 
            //I don't know if it is an issue here or in the html
            $('#bookinfo').append("<input type='hidden' value="+ui.item.title+" name='title'>");
            $('#bookinfo').append("<input type='hidden' value= " + ui.item.author + " name='author'>");
            $('#bookinfo').append("<input type='hidden' value=" +ui.item.publisher+ " name='publisher'>");
            $('#bookinfo').append("<input type='hidden' value=" +ui.item.isbn[0].identifier+" name='ISBN'>");
            
        },
        minLength: 4 // set minimum length of text the user must enter
    });
});