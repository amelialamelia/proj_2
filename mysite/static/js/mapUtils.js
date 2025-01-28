let map = L.map('map').setView([52.0, 19.0], 6);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

function stationsPopupContent(feature) {
    return (
        `<b>Typ stacji: ${feature.properties.type}</b><br>
        <b>Lokalizacja: ${feature.properties.name}</b><br>
        <b>Data założenia: ${feature.properties.activitype}</b><br>`
    )
}

function getStationsLayer(stations_data){
    let stationsLayer = L.geoJSON(stations_data, {
        onEachFeature: (feature, layer) => {
            layer.bindPopup(stationsPopupContent(feature))
        }
    })
    return stationsLayer
}

function getColorBasedOnValue(value){
    if (value < -12){
        return 'red'
    }
    if (value > -12 && value < -6){
        return 'yellow'
    }
    return 'green'
}

function getZagrozenieLabel(value) {
    if (value < -12) {
        return 'Duże'
    }
    if (value >= -12 && value < -6) {
        return 'Średnie'
    }
    return 'Małe'
}

function suszaPopupContent(feature){
    const zagrozenie = getZagrozenieLabel(feature.properties.wskaznik)
    return (
        `<b>Województwo ${feature.properties.name}</b><br>
        <b>Zagrożenie suszy: ${zagrozenie}</b><br>`
    )
}

function getSuszaLayer(susza_data){
    let suszaLayer = L.geoJSON(susza_data, {
        style: function(feature) {
            const color = getColorBasedOnValue(feature.properties.wskaznik)
            return {
                fillColor: color,
                color: '#000',
                weight: 1,
                opacity: 0.7,
                fillOpacity: 0.5
            };
        },
        onEachFeature: (feature, layer) => {
            layer.bindPopup(suszaPopupContent(feature));
        }
    });
    return suszaLayer
}