window.onload = function(){
    parameters=document.getElementById('member-add');
    var addField=document.getElementById('addField');
    if(document.getElementById('add-files'))
    {
      document.getElementById('add-files').addEventListener("click", function()
      {
          // Create the input fields
          var csv = document.createElement('input');
          var nextline=document.createElement("br");

          // Assign attributes to the fields

          csv.setAttribute('name', 'csv');
          csv.setAttribute('type', 'file');

          parameters.appendChild(csv);
          parameters.appendChild(nextline);
      });
    }


}
