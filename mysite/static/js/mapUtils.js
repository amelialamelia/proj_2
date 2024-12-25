let map = L.map('map').setView([52.0, 19.0], 6);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

function getStationsLayer(stations_json){
    stations_layer = L.layerGroup();
    jQuery.each(stations_json, function(i, val) {
        let marker = L.marker([val.lat, val.lng]).addTo(map);
        popupContent = `
            <b>Typ stacji: ${val.type}</b><br>
            <b>Lokalizacja: ${val.name}</b><br>
            <b>Data założenia: ${val.activitype}</b><br>
        `;
        marker.bindPopup(popupContent);
        stations_layer.addLayer(marker);
    });
    return stations_layer;
}

function getSuszaLayers(susza_data){
    woj_layer = L.layerGroup();
    pow_layer = L.layerGroup();
    
    const wojRegex = /^Województwo.*/;
    const powRegex = /^Powiat.*/;
    
    jQuery.each(susza_data, function(i, val) {
        if(wojRegex.test(val.id)){
            console.log("Województwo: " + val.id);
        }
        else if(powRegex.test(val.id)){
            console.log("Powiat: " + val.id);
        }
    });
    return [woj_layer, pow_layer];
}

function linearInterpolation(start, end, percentage){
    return start + Math.round(percentage * (end - start));
}

function colorInterpolation(start, end, value){
    return {
        "r": linearInterpolation(start.r, end.r, value),
        "g": linearInterpolation(start.g, end.g, value),
        "b": linearInterpolation(start.b, end.b, value)
    }
}

function gradientPick(value, start, center, end){
    if(value <50){
        return colorInterpolation(start, center, value*2);
    }
    else if (value == 50){
        return center;
    }
    else{
        return colorInterpolation(center, end, (value-50)*2);
    }
}