function uploadFile() {
    const fileInput = document.getElementById('fileToUpload');
    const file = fileInput.files[0];

    if (!file) {
        alert('Por favor, selecione um arquivo.');
        return;
    }

    const reader = new FileReader();
    reader.onload = function(event) {
        const csvData = event.target.result;
        sendData(csvData);
    };
    reader.readAsText(file);
}

function sendData(csvData) {
    fetch('/process_csv', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ data: csvData })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error('Erro:', data.error);
            document.getElementById('results').innerHTML = 'Erro ao processar os dados: ' + data.error;
        } else {
            document.getElementById('results').innerHTML = data.result;
            document.getElementById('exportButton').classList.remove('hidden');
        }
    })
    .catch(error => console.error('Erro:', error));
}

function exportToExcel() {
    fetch('/export_excel', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ data: document.getElementById('results').innerHTML })
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'dados_filtrados.xlsx';  // Use extensão .xlsx
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    })
    .catch(error => console.error('Erro:', error));
}

document.getElementById('exportButton').addEventListener('click', exportToExcel);