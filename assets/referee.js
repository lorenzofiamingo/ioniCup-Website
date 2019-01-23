window.onload = function () {
    html2canvas(document.getElementById('capture')).then(function(canvas) {
        // Export canvas as a blob
        canvas.toBlob(function(blob) {
            // Generate file download
            window.saveAs(blob, "referto.png");
        });
    });
}
