window.onload = function(){
    parameters=document.getElementById('member-add');
    var addField=document.getElementById('addField');
    if(document.getElementById('add-field'))
    {
      document.getElementById('add-field').addEventListener("click", function()
      {
          // Create the input fields
          var ic_no = document.createElement('input');
          var ref_no_date = document.createElement('input');
          var nextline=document.createElement("br");
          var nextline2=document.createElement("br");
          var nextline3=document.createElement("br");

          // Assign attributes to the fields

          ic_no.className = "ic_no";
          ref_no_date.className = "ref_no_date"

          ic_no.placeholder = "Enter IC Number";
          ref_no_date.placeholder = "Enter Ref No. / Date";

          ic_no.setAttribute('name', 'ic_no');
          ic_no.setAttribute('type', 'text');
          ic_no.setAttribute('style', 'width:10.5cm');

          // ic_no.setAttribute('class', "form-control");


          ref_no_date.setAttribute('name', 'ref_no_date');
          ref_no_date.setAttribute('type', 'text');
          ref_no_date.setAttribute('style', 'width: 10.5cm');

          // ref_no_date.setAttribute('class', "form-control");


          // Add the fields
          parameters.appendChild(ic_no);
          parameters.appendChild( document.createTextNode( '\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0' ) );
          parameters.appendChild(ref_no_date);

          parameters.appendChild(nextline);
          parameters.appendChild(nextline2);


      });
    }


    if(document.getElementById('add-field-non-member'))
    {

      document.getElementById('add-field-non-member').addEventListener("click", function()
      {
          // Create the input fields
          var ic_no = document.createElement('input');
          var name = document.createElement('input');
          var div = document.createElement('input');
          var ref_no_date = document.createElement('input');

          var nextline=document.createElement("br");

          // Assign attributes to the fields
          ic_no.className = "ic_no";
          name.className = "name";
          div.className = "div";
          ref_no_date.className = "ref_no_date"

          ic_no.placeholder = "Enter IC Number";
          name.placeholder = "Enter Name";
          div.placeholder = "Enter Div. / Group";
          ref_no_date.placeholder = "Enter Ref No. / Date";

          ic_no.setAttribute('name', 'ic_no');
          ic_no.setAttribute('type', 'text');

          name.setAttribute('name', 'name');
          name.setAttribute('type', 'text');

          div.setAttribute('name', 'div');
          div.setAttribute('type', 'text');

          ref_no_date.setAttribute('name', 'ref_no_date');
          ref_no_date.setAttribute('type', 'text');

          // Add the fields
          parameters.appendChild(ic_no);
          parameters.appendChild(name);
          parameters.appendChild(div);
          parameters.appendChild(ref_no_date);

          parameters.appendChild(nextline);

      });
    }

}
