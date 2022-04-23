var $fileInput = $('.file-input');

// change inner text
$fileInput.on('change', function() {
  var filesCount = $(this)[0].files.length;
  var $textContainer = $(this).prev();

  if (filesCount === 1) {
    // if single file is selected, show file name
    var fileName = $(this).val().split('\\').pop();
    if (fileName.length > 15) {
        fileName = fileName.slice(0, 12) + '...';
    }
    $textContainer.text(fileName);
  } else {
    // otherwise show number of files
    $textContainer.text(filesCount + ' файлов выбрано');
  }
});