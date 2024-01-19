window.onload = function() {
    var today = new Date();
    var year = today.getFullYear();
    var month = today.getMonth() + 1; // JavaScriptの月は0から始まるため
    var day = today.getDate();
    
    var cells = document.getElementsByTagName('td');
    for (var i = 0; i < cells.length; i++) {
        var cell = cells[i];
        if (cell.dataset.date) {
            var date = new Date(cell.dataset.date);
            if (date.getFullYear() === year && date.getMonth() + 1 === month && date.getDate() === day) {
                cell.classList.add('today');
            }
        }
    }
};
