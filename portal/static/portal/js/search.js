$( function he() {
  alert('he')

  var data = $.ajax( {
    type: 'GET',
    url: `/hello`,
    data: {
    },
    success: function(data){

      book_names = []
      names = ""

      data.forEach(function(biblio) {
        book_names.push(biblio.fields.title)
        names = names + "<li>" + biblio.fields.title + "</li>"
        })

        $( "#search-books" ).autocomplete({
          source: book_names
        });

        document.getElementById("search-results").innerHTML = names;
    }

  })



  var availableTags = [
    "ActionScript",
    "AppleScript",
    "Asp",
    "BASIC",
    "C",
    "C++",
    "Clojure",
    "COBOL",
    "ColdFusion",
    "Erlang",
    "Fortran",
    "Groovy",
    "Haskell",
    "Java",
    "JavaScript",
    "Lisp",
    "Perl",
    "PHP",
    "Python",
    "Ruby",
    "Scala",
    "Scheme"
  ];
  // $( "#search-books" ).autocomplete({
  //   source: availableTags
  // });
} );























function searcher()
{
  var text = document.getElementById('book_search');
  // last_key = event.keycode || event.which // Depends on browser - Firefox does not support keycode
  // last_char = String.fromCharCode(parseInt(last_key))
  // alert(last_char);
  // alert(text.value)
  text = text.value
  console.log('checking')
  if(text.length>2)
  {
    var data = $.ajax( {
      type: 'GET',
      url: `/hello`,
      data: {
        'search_text':text
      },
      success: function(data){
        if( data.length==0 )
        {
          console.log('Happened')
          names = "<li>Sorry, no book found</li>"
        }
        else
        {
          book_names = []
          names = ""

          data.forEach(function(biblio) {
            book_names.push(biblio.fields.title)
            names = names + "<li>" + biblio.fields.title + "</li>"
          })
        }


          document.getElementById("search-results").innerHTML = names;
      }

    })
  }
};
