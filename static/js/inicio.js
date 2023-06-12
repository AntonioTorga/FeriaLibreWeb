

let map = L.map("map").setView([-33.45767214984646, -70.66448391627137], 4);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{
maxZoom:20,
attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

fetch('http://localhost:5000/get-map-data')
.then(response => response.json())
 .then(data => {
    for(let k in data){
        let donaciones = data[k]['donaciones']
        let text = ""
        if (donaciones != null){
            text = text + "<h3>Donaciones: </h3>"
            for (let donacion in donaciones){
                console.log(donaciones[donacion])
                text= text + ("ID Donacion: " + donaciones[donacion]['id'] + "<br> Tipo: "+ donaciones[donacion]["tipo"]+ "<br> Cantidad: "+ donaciones[donacion]["cantidad"]+"<br> Fecha de disponibilidad: "+ donaciones[donacion]["fecha_disponibilidad"]+ " <br>Calle y número: "+ donaciones[donacion]["calle_numero"] + "<br> Email: "+ donaciones[donacion]["email"]+"<br><br>")
            }
        }
        let text_2 = ""
        let pedidos = data[k]['pedidos']
        if (pedidos != null){
            text_2 = "<h3>Pedidos:</h3>"
            for (let pedido in pedidos){
                text_2= text_2 + ("<p>Pedido: " + pedidos[pedido]['id'] + "<br> Tipo: "+ pedidos[pedido]["tipo"] + "<br> Cantidad: "+ pedidos[pedido]["cantidad"]+ "<br> Email: "+ pedidos[pedido]["email"]+"<br><br>")
            }
        }
        if(text!=""){
            const onMarkerClick = (e) => {
            L.popup()
                .setLatLng([data[k]['lat'], data[k]['lng']])
                    .setContent(text)
                    .openOn(map);
            }
            let marker = L.marker([data[k]['lat'], data[k]['lng']]).addTo(map).on('click', onMarkerClick);
        }
        if(text_2!=""){
            var greenIcon = new L.Icon({
                iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
                shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                iconSize: [25, 41],
                iconAnchor: [12, 41],
                popupAnchor: [1, -34],
                shadowSize: [41, 41]
              });
            let close_ubic = [parseFloat(data[k]['lat'])+0.01, parseFloat(data[k]['lng'])+0.01]
            const onMarkerClick = (e) => {
            L.popup()
                .setLatLng(close_ubic)
                    .setContent(text_2)
                    .openOn(map);
            }
            let marker = L.marker(close_ubic,{icon: greenIcon}).addTo(map).on('click', onMarkerClick);
        }
    }
 })
