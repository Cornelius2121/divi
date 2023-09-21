function getAddedNameValue() {
    var x = document.getElementById("frm1");
    var text = "";
    var i;
    for (i = 0; i < x.length; i++) {
        text += x.elements[i].value;
    }
    // Get the table element in which you want to add row
    let table = document.getElementById("names");

    // Create a row using the inserRow() method and
    // specify the index where you want to add the row
    let row = table.insertRow(-1); // We are adding at the end

    // Create table cells
    let c1 = row.insertCell(0);
    c1.innerText = text;

    // Add the data as rule options
    var buyer = document.getElementById("buyer");
    var buyee = document.getElementById("buyee");
    var opt = document.createElement('option');
    opt.value = text;
    opt.innerHTML = text;
    buyer.appendChild(opt);
    var opt = document.createElement('option');
    opt.value = text;
    opt.innerHTML = text;
    buyee.appendChild(opt);

    // Add the data as rule options
    var buyer = document.getElementById("buyer_forever");
    var buyee = document.getElementById("buyee_forever");
    var opt = document.createElement('option');
    opt.value = text;
    opt.innerHTML = text;
    buyer.appendChild(opt);
    var opt = document.createElement('option');
    opt.value = text;
    opt.innerHTML = text;
    buyee.appendChild(opt);

    // Reset the form
    document.getElementById("frm1").reset();
    ``
}

function addYear() {
    var x = document.getElementById("frm4");
    var yearInput = x.elements[0].value;
    // Add the data as rule options
    var year = document.getElementById("year");
    var opt = document.createElement('option');
    opt.value = yearInput;
    opt.innerHTML = yearInput;
    year.appendChild(opt);
    // Reset the form
    document.getElementById("frm4").reset();
}

function addForeverRule() {
    var x = document.getElementById("frm5");
    var personA = x.elements[0].value;
    var personB = x.elements[1].value;
    var reverse = x.elements[2].checked;
    if (personB === personA) {
        alert("You can't buy for yourself!");
        // Reset the form
        document.getElementById("frm5").reset();
        return;
    }
    // Get the table element in which you want to add row
    let table = document.getElementById("forever_rules");

    // Create a row using the inserRow() method and
    // specify the index where you want to add the row
    let row = table.insertRow(-1); // We are adding at the end

    // Create table cells
    let c1 = row.insertCell(0);
    c1.innerText = personA;
    let c2 = row.insertCell(1);
    c2.innerText = personB;

    if (reverse) {
        let row = table.insertRow(-1); // We are adding at the end

        // Create table cells
        let c1 = row.insertCell(0);
        c1.innerText = personB;
        let c2 = row.insertCell(1);
        c2.innerText = personA;
    }

    // Reset the form
    document.getElementById("frm5").reset();
}

function addRule() {
    var x = document.getElementById("frm3");
    var personA = x.elements[0].value;
    var personB = x.elements[1].value;
    var year = x.elements[2].value;
    if (personB === personA) {
        alert("You can't buy for yourself!");
        // Reset the form
        document.getElementById("frm3").reset();
        return;
    }
    // Get the table element in which you want to add row
    let table = document.getElementById("rules");

    // Create a row using the inserRow() method and
    // specify the index where you want to add the row
    let row = table.insertRow(-1); // We are adding at the end

    // Create table cells
    let c1 = row.insertCell(0);
    c1.innerText = personA;
    let c2 = row.insertCell(1);
    c2.innerText = personB;
    let c3 = row.insertCell(2);
    c3.innerText = year;

    // Reset the form
    document.getElementById("frm3").reset();
}

function createAllocation() {
    var allocation = [];
    let people = [];
    var table = document.getElementById("names");
    for (i = 1; i < table.rows.length; i++) {
        var personA = table.rows[i].cells[0].innerHTML;
        people.push(personA);
    }
    allocation.push({
        "people": people
    });
    var table = document.getElementById("rules");
    var i;
    var count = document.getElementById("number_to_buy").value;
    allocation.push({
        "count": count
    });
    let rules = [];
    for (i = 1; i < table.rows.length; i++) {
        var personA = table.rows[i].cells[0].innerHTML;
        var personB = table.rows[i].cells[1].innerHTML;
        var year = table.rows[i].cells[2].innerHTML;
        rules.push({
            "personA": personA,
            "personB": personB,
            "Year": year
        });
    }
    var table = document.getElementById("forever_rules");
    for (i = 1; i < table.rows.length; i++) {
        var personA = table.rows[i].cells[0].innerHTML;
        var personB = table.rows[i].cells[1].innerHTML;
        rules.push({
            "personA": personA,
            "personB": personB,
        });
    }
    allocation.push({
        "rules": rules
    });
    $.ajax({
        type: "POST",
        url: '/create',
        async: false,
        data: JSON.stringify(allocation),
        contentType: "application/json",
        success: function (data) {
            window.location.href = "/allocation";
        }, fail: function () {

        }
    })
}