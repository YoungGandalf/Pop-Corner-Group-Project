let map;

function initMap() {
    var center = { lat: 39.2550, lng: -76.7076 };

    var locations = [
        ['R/C Hollywood Cinema 4', 39.24730343739293, -76.69362005212618],
        ['The Y in Catonsville', 39.25341163767778, -76.7276237518471],
        ['The Hub Asian Food Hall', 39.28771380004267, -76.7616886293824],
        ['Depaola\'s Pub', 39.254894508952475, -76.69666547387196],
        ['Catonsville Community Park', 39.27867498196773, -76.75307346147278],
        ['Erickson Field', 39.25713811685214, -76.71052874416344],
    ];

    map = new google.maps.Map(document.getElementById("map"), {
        center: center,
        zoom: 13,
    });

    for (var i = 0; i < locations.length; i++){
        var place = locations[i];
        var myLatLng = new google.maps.LatLng(place[1], place[2]);
        var marker = new google.maps.Marker({
            position: myLatLng,
            map: map,
            url: "/reservation",
            title: place[0]
        });

        google.maps.event.addListener(marker, 'onmouseover', function(){
            infowindow.setContent(marker.title);
            infowindow.open(map, marker);
        })

        google.maps.event.addListener(marker, 'click', function(){
            window.location.href = marker.url;
        });
    }
}