

   var faqs_row = 0;
   function addfaqs() {
    html  = '<tr id="faqs-row' + faqs_row + '">';
  html += '<td><input type="text" class="form-control" placeholder="User name"></td>';
  html += '<td><input type="text" placeholder="Product name" class="form-control" ></td>';
  html += '<td class="text-danger mt-10"> 18.76% <i class="fa fa-arrow-down"></i></td>';
  html += '<td class="mt-10"><button class="badge badge-danger" onclick="$(\'#faqs-row' + faqs_row + '\').remove();"><i class="fa fa-trash"></i> Delete</button></td>';

  html += '</tr>';

  $('#faqs tbody').append(html);

  faqs_row++;
} 
    