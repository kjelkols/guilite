// Automatisk beregning ved endring av input hvis avkrysset
document.addEventListener("DOMContentLoaded", function() {
    var autoCalc = document.getElementById("autoCalc");
    var form = document.getElementById("sideform");
    // Hent tidligere valg fra localStorage
    if (autoCalc) {
        var saved = localStorage.getItem('autoCalcChecked');
        if (saved === null) {
            autoCalc.checked = true; // default første gang
        } else {
            autoCalc.checked = saved === 'true';
        }
        autoCalc.addEventListener('change', function() {
            localStorage.setItem('autoCalcChecked', autoCalc.checked);
        });
    }
    function autoCalcHandler(e) {
        if (autoCalc && autoCalc.checked) {
            // Ikke trigge på simulator-velger eller filopplasting
            if (e.target.name && e.target.name !== "simulator" && e.target.type !== "file") {
                form.requestSubmit();
            }
        } else {
            // Hvis automatisk beregning ikke er aktiv, fjern kun rapportresultat fra skjermen
            if (e.target.name && e.target.name !== "simulator" && e.target.type !== "file") {
                var reportDiv = document.getElementById('report_html_container');
                if (reportDiv) {
                    reportDiv.innerHTML = '';
                }
            }
        }
    }
    if (form && autoCalc) {
        form.addEventListener("input", autoCalcHandler);
        // Kjør automatisk beregning kun én gang ved første lasting hvis avkrysset og det er første GET (firstLoad==1)
        var firstLoad = document.getElementById('firstLoad');
        if (autoCalc.checked && firstLoad && firstLoad.value === '1') {
            setTimeout(function() {
                form.requestSubmit();
            }, 100);
        }
    }
});
// Legg til event listener for filopplasting når DOM er klar
document.addEventListener("DOMContentLoaded", function() {
    var uploadInput = document.getElementById("uploadInputFile");
    if (uploadInput) {
        uploadInput.addEventListener("change", function() {
            window.uploadInputFile(this);
        });
    }
});
window.downloadInput = function() {
    const data = window.input_json;
    const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'input.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

window.uploadInputFile = function(input) {
    const inputFields = window.input_fields;
    console.log('uploadInputFile called', input);
    if (!input.files || !input.files[0]) {
        console.log('No file selected');
        return;
    }
    const file = input.files[0];
    console.log('Selected file:', file);
    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            console.log('File loaded, content:', e.target.result);
            const json = JSON.parse(e.target.result);
            console.log('Parsed JSON:', json);
            let missing = [];
            let updated = [];
            inputFields.forEach(function(field) {
                if (json.hasOwnProperty(field)) {
                    const el = document.getElementsByName(field)[0];
                    if (el) {
                        el.value = json[field];
                        updated.push(field);
                        console.log('Set value for', field, 'to', json[field]);
                    } else {
                        console.log('No input element found for', field);
                    }
                } else {
                    missing.push(field);
                }
            });
            // Finn felter i json som ikke finnes i inputFields
            let extra = Object.keys(json).filter(function(key) { return !inputFields.includes(key); });
            let msg = 'Oppdaterte verdier for: ' + (updated.length > 0 ? updated.join(', ') : '(ingen)') + '\n';
            if (missing.length > 0) {
                msg += 'Følgende felter i skjemaet ble ikke oppdatert: ' + missing.join(', ') + '\n';
            } else {
                msg += 'Alle felter i skjemaet ble oppdatert.\n';
            }
            if (extra.length > 0) {
                msg += 'Felter i filen som ikke finnes i skjemaet: ' + extra.join(', ');
            }
            alert(msg);
        } catch (err) {
            alert('Kunne ikke lese JSON: ' + err);
            console.log('JSON parse error:', err);
        }
        input.value = '';
    };
    reader.readAsText(file);
}
