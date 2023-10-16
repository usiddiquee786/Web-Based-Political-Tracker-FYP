
var map = L.map('map').setView([30, 75], 5);
var osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {

});
osm.addTo(map);
// Google Map Layer

googleStreets = L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
    maxZoom: 20,
    subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
});
googleStreets.addTo(map);


//Colors
function getColor(d) {
    return d > 1000 ? '#800026' :
        d > 500 ? '#BD0026' :
            d > 200 ? '#E31A1C' :
                d > 100 ? '#FC4E2A' :
                    d > 600 ? '#FD8D3C' :
                        d > 700 ? '#FEB24C' :
                            d > 30 ? '#FEB24C' :
                                '#000';
}

function style(feature) {
    return {
        fillColor: getColor(feature.properties.MNA),
        weight: 1,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.5
    };
}
L.geoJson(AllProvince, { style: style }).addTo(map);

function highlightFeature(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 2,
        color: 'white',
        dashArray: '',
        fillOpacity: 0.1
    });

    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
        layer.bringToFront();
    }

    info.update(layer.feature.properties);
}
function resetHighlight(e) {
    geojson.resetStyle(e.target);
    info.update();
}
var geojson;
// ... our listeners
geojson = L.geoJson(AllProvince);
function zoomToFeature(e) {
    map.fitBounds(e.target.getBounds());
}

function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: zoomToFeature
    });
}



var info = L.control();

info.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
    // var div2 = L.DomUtil.create('div', 'info1'); // create a second div with a class "info1"
    // this._div.parentNode.insertBefore(div2, this._div.nextSibling); // insert the second div after the first div

    this.update();
    return this._div;
};


// method that we will use to update the control based on feature properties passed
info.update = function (props) {
    this._div.innerHTML = '<h4>This map shows the<br/>Number of Official Members<br/> of Political Parties<br/> who tweeted<br> Select Party</h4><h5>*You may select multiple parties*</h5>';

};
info.addTo(map);

var Party = [];
var flag = false;
var PartySum;
var checked = []
//Uncheck funtion
function uncheckAll() {
    const selectedOptionsP = document.querySelectorAll('input.item[type=checkbox]:checked');
    selectedOptionsP.forEach(option => {
        option.checked = false;
    });
    var btnText = document.querySelector(".btn-text");
    btnText.innerText = "Select Topic";
    checked = document.querySelectorAll(".non-existent-class");
    console.log(checked.length)
    let items = document.querySelectorAll(".item");
    items.forEach(item => {
        item.classList.remove("checked")
    })

}

//CheckedDropdownJS Topic moved from index.html
const items = document.querySelectorAll(".item");
items.forEach(item => {
    item.addEventListener("click", () => {
        item.classList.toggle("checked");

        checked = document.querySelectorAll(".checked"),
            btnText = document.querySelector(".btn-text");
        if (checked && checked.length > 0) {
            console.log(checked.length)
            btnText.innerText = `${checked.length} Selected`;
        } else {
            console.log(checked.length)
            btnText.innerText = "Select Topic";
        }
    });
})
var PartyName;
var datap;
var partyValues = [];
//CheckedDropDownListParty
var CheckedDropDownListParty = document.getElementById('checkBoxesP');
CheckedDropDownListParty.onchange = (ev) => {
    var partyCheckboxes = document.querySelectorAll("#checkBoxesP input[type='checkbox']:checked");

    for (var i = 0; i < partyCheckboxes.length; i++) {
        partyValues.push(partyCheckboxes[i].value);
    }
    // alert(partyValues)
    // datap = new URLSearchParams();
    // datap.append(JSON.stringify(partyValues));
    var xhr = new XMLHttpRequest();
    // const decodedData = decodeURIComponent(data);
    // alert(decodedData)
    xhr.open("GET", "/parties", true);
    xhr.onreadystatechange = function () {
        //alert("umar")
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            console.log("I'm Here")
            // Parse the JSON response from the server
            var data = JSON.parse(xhr.responseText);

            // Update the relevant HTML elements with the retrieved data
            // etc
            //alert(data)

            var selectedOptionsP = document.querySelectorAll('input.itemP[type=checkbox]:checked');
            var unSelectedOptionsP = document.querySelectorAll('input.itemP[type=checkbox]:not(:checked)');
            console.log(unSelectedOptionsP);
            var checkedArrayP = [];
            var unCheckedArrayP = [];

            for (var i = 0; i < selectedOptionsP.length; i++) {
                checkedArrayP[i] = selectedOptionsP[i].value
                // unCheckedArrayP[i]=unSelectedOptionsP[i].value
            }
            PartyName = checkedArrayP;
            //alert(typeof PartyName)
            flag = true;
            if (PartyName.includes('PTI') || PartyName.includes('PMLN') || PartyName.includes('PPP')) {
                var sortedParty = PartyName.sort();
                var n_ptimemberBAL = data.n_ptimemberBAL;
                var n_pmlnmemberBAL = data.n_pmlnmemberBAL;
                var pti_tweetBAL = data.pti_tweetBAL;
                var pmln_tweetBAL = data.pmln_tweetBAL;
                var n_ptimemberISL = data.n_ptimemberISL;
                var n_pmlnmemberISL = data.n_pmlnmemberISL;
                var pti_tweetISL = data.pti_tweetISL;
                var pmln_tweetISL = data.pmln_tweetISL;
                var n_ptimemberSI = data.n_ptimemberSI;
                var n_pmlnmemberSI = data.n_pmlnmemberSI;
                var pti_tweetSI = data.pti_tweetSI;
                var pmln_tweetSI = data.pmln_tweetSI;
                var n_ptimemberPJ = data.n_ptimemberPJ;
                var n_pmlnmemberPJ = data.n_pmlnmemberPJ;
                var pti_tweetPJ = data.pti_tweetPJ;
                var pmln_tweetPJ = data.pmln_tweetPJ;
                var n_ptimemberKP = data.n_ptimemberKP;
                var n_pmlnmemberKP = data.n_pmlnmemberKP;
                var pti_tweetKP = data.pti_tweetKP;
                var pmln_tweetKP = data.pmln_tweetKP;
                var PPPvalues = 33
                var ptitweet = data.pti_tweet
                var pmlntweet = data.pmln_tweet
                info.update = function (props) {
                    for (var k = 0; k < sortedParty.length; k++) {
                        if (sortedParty[k] == 'PMLN' && sortedParty[k + 1] == 'PPP' && sortedParty[k + 2] == 'PTI') {
                            // console.log(sortedParty[k]+sortedParty[k+1]+sortedParty[k+2]);       
                            this._div.innerHTML = '<h4>Number of Offical Members <br/> of PTI and their Tweets <br/>in each Province</h4><br/>' + (props ?
                                ((props.shapeName === "BAL") ?
                                    '<b>' + 'Balochistan' + '</b><br/>' + n_ptimemberBAL + ' Official Members<br/>' + pti_tweetBAL + ' Tweets<hr><h4>Number of Official Members<br/>of PMLN and their Tweets<br/>in each Province</h4>' +
                                    '<b>' + 'Balochistan' + '</b><br/>' + n_pmlnmemberBAL + ' Official Members<br/>' + pmln_tweetBAL + ' Tweets<hr><h4>Number of Official Members<br/>of PPP and their Tweets<br/>in each Province</h4>' +
                                    '<b>' + 'Balochistan' + '</b><br/>' + PPPvalues + ' Official Members<br/>' + PTIvalues + ' Tweets<hr>'
                                    : ((props.shapeName === "Islamabad") ?
                                        '<b>' + props.shapeName + '</b><br/>' + n_ptimemberISB + ' Official Members<br/>' + pti_tweetISB + ' Tweets<hr><h4>Number of Official Members<br/>of PMLN and their Tweets<br/>in each Province</h4>' +
                                        '<b>' + props.shapeName + '</b><br/>' + n_pmlnmemberISB + ' Official Members<br/>' + pmln_tweetISB + ' Tweets<hr><h4>Number of Official Members<br/>of PPP and their Tweets<br/>in each Province</h4>' +
                                        '<b>' + props.shapeName + '</b><br/>' + PPPvaluesISB + ' Official Members<br/>' + PTIvaluesISB + ' Tweets<hr>'
                                        : ((props.shapeName === "Sindh") ?
                                            '<b>' + props.shapeName + '</b><br/>' + n_ptimemberSI + ' Official Members<br/>' + pti_tweetSI + ' Tweets<hr><h4>Number of Official Members<br/>of PMLN and their Tweets<br/>in each Province</h4>' +
                                            '<b>' + props.shapeName + '</b><br/>' + n_pmlnmemberSI + ' Official Members<br/>' + pmln_tweetSO + ' Tweets<hr><h4>Number of Official Members<br/>of PPP and their Tweets<br/>in each Province</h4>' +
                                            '<b>' + props.shapeName + '</b><br/>' + 0 + ' Official Members<br/>' + 0 + ' Tweets<hr>'
                                            : 'Hover over a province<hr><h4>Number of Official Members<br/>of PMLN and their Tweets<br/>in each Province</h4>' + (props ?
                                                '<b>' + props.shapeName + '</b><br/>' + PMLNvalues + ' Official Members<br/>' + pmlntweet + ' Tweets<hr>'
                                                : 'Hover over a province<hr><h4>Number of Official Members<br/>of PPP and their Tweets<br/>in each Province</h4>' + (props ?
                                                    '<b>' + props.shapeName + '</b><br/>' + PPPvalues + ' Official Members<br/>' + PTIvalues + ' Tweets<hr>'
                                                    : 'Hover over a province<hr>')))))
                                : 'Hover over a province<hr><h4>Number of Official Members<br/>of PMLN and their Tweets<br/>in each Province</h4>' +
                                '<b>' + props.shapeName + '</b><br/>' + PMLNvalues + ' Official Members<br/>' + pmlntweet + ' Tweets<hr><h4>Number of Official Members<br/>of PPP and their Tweets<br/>in each Province</h4>' +
                                '<b>' + props.shapeName + '</b><br/>' + PPPvalues + ' Official Members<br/>' + PTIvalues + ' Tweets<hr>');
                            break;
                        }
                        else if (sortedParty[k] == 'PMLN' && sortedParty[k + 1] == 'PTI') {
                            // console.log(sortedParty[k]+sortedParty[k+1]);
                            this._div.innerHTML = '<h4>Number of Offical Members <br/> of PTI and their Tweets <br/> in each Province</h4>' + (props ?
                                ((props.shapeName === "BAL") ?
                                    '<b>' + 'Balochistan' + '</b><br />' + n_ptimemberBAL + ' Official Members<br />' + pti_tweetBAL + ' Tweets<hr> <h4>Number of Offical Members <br/> of PMLN and their Tweets <br/> in each Province</h4>' +
                                    '<b>' + 'Balochistan' + '</b><br />' + n_pmlnmemberBAL + ' Official Members<br />' + pmln_tweetBAL + ' Tweets'
                                    : ((props.shapeName === "ISL") ?
                                        '<b>' + 'Islamabad Capital Territory' + '</b><br />' + n_ptimemberISL + ' Official Members<br />' + pti_tweetISL + ' Tweets<hr> <h4>Number of Offical Members <br/> of PMLN and their Tweets <br/> in each Province</h4>' +
                                        '<b>' + 'Islamabad Capital Territory' + '</b><br />' + n_pmlnmemberISL + ' Official Members<br />' + pmln_tweetISL + ' Tweets'
                                        : ((props.shapeName === "PJ") ?
                                            '<b>' + 'Punjab' + '</b><br />' + n_ptimemberPJ + ' Official Members<br />' + pti_tweetPJ + ' Tweets<hr> <h4>Number of Offical Members <br/> of PMLN and their Tweets <br/> in each Province</h4>' +
                                            '<b>' +'Punjab' + '</b><br />' + n_pmlnmemberPJ + ' Official Members<br />' + pmln_tweetPJ + ' Tweets'
                                            : ((props.shapeName === "SI") ?
                                                '<b>' + 'Sindh' + '</b><br />' + n_ptimemberSI + ' Official Members<br />' + pti_tweetSI + ' Tweets<hr> <h4>Number of Offical Members <br/> of PMLN and their Tweets <br/> in each Province</h4>' +
                                                '<b>' + 'Sindh' + '</b><br />' + n_pmlnmemberSI + ' Official Members<br />' + pmln_tweetSI + ' Tweets'
                                                : ((props.shapeName === "KP") ?
                                                    '<b>' + 'Khyber Pakhtunkhwa' + '</b><br />' + n_ptimemberKP + ' Official Members<br />' + pti_tweetKP + ' Tweets<hr> <h4>Number of Offical Members <br/> of PMLN and their Tweets <br/> in each Province</h4>' +
                                                    '<b>' + 'Khyber Pakhtunkhwa' + '</b><br />' + n_pmlnmemberKP + ' Official Members<br />' + pmln_tweetKP + ' Tweets'
                                                    : 'Hover over a province')))))
                                : 'Hover over a province');
                            break;
                        }
                        else if (sortedParty[k] == 'PMLN' && sortedParty[k + 1] == 'PPP') {
                            // console.log(sortedParty[k]+sortedParty[k+1]);
                            this._div.innerHTML = '<h4>Number of Offical Members <br/> of PMLN and their Tweets <br/> in each Province</h4>' + (props ?
                                '<b>' + props.shapeName + '</b><br />' + PMLNvalues + ' Official Members<br />' + pmlntweet + ' Tweets <hr><h4>Number of Offical Members <br/> of PPP and their Tweets <br/> in each Province</h4>' +
                                '<b>' + props.shapeName + '</b><br />' + PPPvalues + ' Official Members<br />' + PTIvalues + ' Tweets'
                                : 'Hover over a province' + '<hr>' + '<h4>Number of Offical Members <br/> of PPP and their Tweets <br/> in each Province</h4>' + (props ?
                                    '<b>' + props.shapeName + '</b><br />' + PPPvalues + ' Official Members<br />' + PTIvalues + ' Tweets<hr> '
                                    : 'Hover over a province'));
                            break;
                        }
                        else if (sortedParty[k] == 'PPP' && sortedParty[k + 1] == 'PTI') {
                            // console.log(sortedParty[k]+sortedParty[k+1]);
                            this._div.innerHTML = '<h4>Number of Offical Members <br/> of PTI and their Tweets <br/> in each Province</h4>' + (props ?
                                '<b>' + props.shapeName + '</b><br />' + PTIvalues + ' Official Members <br />' + ptitweet + ' Tweets<hr> <h4>Number of Offical Members <br/> of PPP and their Tweets <br/> in each Province</h4>' +
                                '<b>' + props.shapeName + '</b><br />' + PPPvalues + ' Official Members<br />' + PTIvalues + ' Tweets'
                                : 'Hover over a province' + '<hr>' + '<h4>Number of Offical Members <br/> of PPP and their Tweets <br/> in each Province</h4>' + (props ?
                                    '<b>' + props.shapeName + '</b><br />' + PPPvalues + ' Official Members<br />' + PTIvalues + ' Tweets<hr> '
                                    : 'Hover over a province'));
                            break;
                        }
                        else if (sortedParty[k] == 'PTI') {
                            // console.log(sortedParty[k]);
                            this._div.innerHTML = '<h4>Number of Offical Members <br/> of PTI and their Tweets <br/> in each Province</h4>' + (props ?
                                ((props.shapeName === "BAL") ?
                                    '<b>' + 'Balochistan' + '</b><br />' + n_ptimemberBAL + ' Official Members' + '<br />' + pti_tweetBAL + ' Tweets'
                                    : ((props.shapeName === "ISL") ?
                                        '<b>' + 'Islamabad Capital Territory' + '</b><br />' + n_ptimemberISL + ' Official Members' + '<br />' + pti_tweetISL + ' Tweets'
                                        : ((props.shapeName === "PJ") ?
                                            '<b>' + 'Punjab' + '</b><br/>' + n_ptimemberPJ + ' Official Members<br/>' + pti_tweetPJ + ' Tweets'
                                            : ((props.shapeName === "SI") ?
                                                '<b>' + 'Sindh' + '</b><br/>' + n_ptimemberSI + ' Official Members<br/>' + pti_tweetSI + ' Tweets'
                                                : ((props.shapeName === "KP") ?
                                                    '<b>' + 'Khyber Pakhtunkhwa' + '</b><br/>' + n_ptimemberKP + ' Official Members<br/>' + pti_tweetKP + ' Tweets'
                                                    : 'Hover over a province')))))
                                : 'Hover over a province');
                        }
                        else if (sortedParty[k] == 'PMLN') {
                            // console.log(sortedParty[k]);
                            this._div.innerHTML = '<h4>Number of Offical Members <br/> of PMLN and their Tweets <br/> in each Province</h4>' + (props ?
                                ((props.shapeName === "BAL") ?
                                    '<b>' + 'Balochistan' + '</b><br />' + n_pmlnmemberBAL + ' Official Members' + '<br />' + pmln_tweetBAL + ' Tweets'
                                    : ((props.shapeName === "ISL") ?
                                        '<b>' + 'Islamabad Capital Territory' + '</b><br />' + n_pmlnmemberISL + ' Official Members' + '<br />' + pmln_tweetISL + ' Tweets'
                                        : ((props.shapeName === "PJ") ?
                                            '<b>' + 'Punjab' + '</b><br/>' + n_pmlnmemberPJ + ' Official Members<br/>' + pmln_tweetPJ + ' Tweets'
                                            : ((props.shapeName === "SI") ?
                                                '<b>' + 'Sindh' + '</b><br/>' + n_pmlnmemberSI + ' Official Members<br/>' + pmln_tweetSI + ' Tweets'
                                                : ((props.shapeName === "KP") ?
                                                    '<b>' + 'Khyber Pakhtunkhwa' + '</b><br/>' + n_pmlnmemberKP + ' Official Members<br/>' + pmln_tweetKP + ' Tweets'
                                                    : 'Hover over a province')))))
                                : 'Hover over a province');
                        }
                        else if (sortedParty[k] == 'PPP') {
                            // console.log(sortedParty[k]);
                            this._div.innerHTML = '<h4>Number of Offical Members <br/> of PPP and their Tweets <br/> in each Province</h4>' + (props ?
                                '<b>' + props.shapeName + '</b><br />' + PPPvalues + ' Official Members' + '<br />' + PTIvalues + ' Tweets'
                                : 'Hover over a province');
                        }
                        else {
                            console.log('brrrrrrrr')
                        }
                    }
                }; info.addTo(map);
            }
        }

    }
    xhr.send();
    if (unSelectedOptionsP.length == 3) {

        info.update = function (props) {
            this._div.innerHTML = '<h4>Select Party</h4><h5>*You may select multiple parties*</h5>';
            Party = [];
        };
        info.addTo(map);
        // console.log('checkedArrayP');

    }
}


var popup = L.popup();

function onMapClick(e) {
    var shapeName = e.target.feature.properties.shapeName;
    if (!PartyName) {
        alert("Please select the party.");
        window.location.href = "/";
    }
    popup   
        // alert(feature.properties.shapeName)
        .setLatLng(e.latlng)
        .setContent('<a href="/analytics?loc='+encodeURIComponent(JSON.stringify(shapeName))+'&parties='+encodeURIComponent(JSON.stringify(PartyName))+'">View Details</a>')
        .openOn(map);
}
geojson = L.geoJson(AllProvince, {
    style: style,
    onEachFeature: function (feature, layer) {
      onEachFeature(feature, layer); // call onEachFeature function first
      layer.on('click', function(e) {
        onMapClick(e); // call onMapClick function on click event
      });
    }
  }).addTo(map);
//   geojson = L.geoJson(AllProvince, {
    
//     onEachFeature: function (feature, layer) {
//     layer.on('click', onMapClick);},
//     style: style,
//     onEachFeature: onEachFeature,
// }).addTo(map);
