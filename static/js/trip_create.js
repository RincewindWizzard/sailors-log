document.addEventListener('DOMContentLoaded', function () {
  const input = document.querySelector('.file-input');
  const fileName = document.getElementById('gpx-file-name');

  if (input) {
    input.addEventListener('change', function () {
      if (input.files.length > 0) {
        fileName.textContent = input.files[0].name;
      } else {
        fileName.textContent = 'Keine Datei ausgewählt';
      }
    });
  }
});