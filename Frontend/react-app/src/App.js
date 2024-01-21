import React, { useEffect, useState, useRef } from 'react';
import { GoogleMap, LoadScript, InfoWindow } from '@react-google-maps/api';
import './App.css';

const center = {
  lat: 45.559212, // Latitude for Montreal 45.500046, -73.666483
  lng: -73.663288 // Longitude for Montreal
};


// Example heatmap data
const heatmapData = [
  { lat: 45.542611, lng: -73.672978, weight: 1, info: 'Ahuntsic-Cartierville' },
  { lat: 45.612864, lng: -73.564033, weight: 1, info: 'Anjou'},
  { lat: 45.480037, lng: -73.621360, weight: 1, info: 'Côte-des-Neiges-Notre-Dame-de-Grâce'},
  { lat: 45.446529, lng: -73.691388, weight: 1, info: 'Lachine'},
  { lat: 45.433639, lng: -73.623949, weight: 1, info: 'LaSalle'},
  { lat: 45.524945, lng: -73.578563, weight: 1, info: 'Le Plateau-Mont-Royal'},
  { lat: 45.472200, lng: -73.584305, weight: 1, info: 'Le Sud-Ouest'},
  { lat: 45.496323, lng: -73.892990, weight: 1, info: 'L\'Île-Bizard-Sainte-Geneviève'},
  { lat: 45.577282, lng: -73.532281, weight: 1, info: 'Mercier-Hochelaga-Maisonneuve'},
  { lat: 45.603972, lng: -73.628525, weight: 1, info: 'Montréal-Nord'},
  { lat: 45.515628, lng: -73.608555, weight: 1, info: 'Outremont' },
  { lat: 45.473283, lng: -73.864399, weight: 1, info: 'Pierrefonds-Roxboro'},
  { lat: 45.659499, lng: -73.521665, weight: 1, info: 'Rivière-des-Prairies-Pointe-aux-Trembles'},
  { lat: 45.551868, lng: -73.579247, weight: 1, info: 'Rosemont-La Petite-Patrie'},
  { lat: 45.500384, lng: -73.708637, weight: 1, info: 'Saint-Laurent'},
  { lat: 45.589129, lng: -73.594911, weight: 1, info: 'Saint-Léonard'},
  { lat: 45.452550, lng: -73.574752, weight: 1, info: 'Verdun' },
  { lat: 45.498876, lng: -73.572779, weight: 1, info: 'Ville-Marie' },
  { lat: 45.566328, lng: -73.615413, weight: 1, info: 'Villeray-Saint-Michel-Parc-Extension' }
];


function App() {
  const [selectedPoint, setSelectedPoint] = useState(null);
  const [crimeData, setCrimeData] = useState({}); // State to hold crime data
  const [heatmapLayers, setHeatmapLayers] = useState([]); // New state to keep track of heatmap layers
  const [scores, setScores] = useState({});
  const mapRef = useRef(null); // Ref to store the Google Map instance

  useEffect(() => {
    fetch('https://protekt-flask-api.onrender.com/additional') // Replace with your Flask API endpoint
      .then(response => response.json())
      .then(data => setCrimeData(data))
      .catch(error => console.error('Error fetching crime data:', error));
  }, []);
  
  // New useEffect for fetching radius data
  useEffect(() => {
    fetch('https://protekt-flask-api.onrender.com/score') // Replace with the new API URL
      .then(response => response.json())
      .then(radiusData => {updateHeatmapRadius(radiusData);
        setScores(radiusData);
      }) // Call to update the heatmap radius
      .catch(error => console.error('Error fetching radius data:', error));
  }, []);

  const updateHeatmapRadius = (newRadiusData) => {
    if (mapRef.current) {
      // Check if heatmap layers have been initialized
      if (heatmapLayers.length === 0) {
        const google = window.google;
        const newLayers = heatmapData.map(point => {
          const newRadius = newRadiusData[point.info] || 20; // Default radius if not in fetched data
          return new google.maps.visualization.HeatmapLayer({
            data: [new google.maps.LatLng(point.lat, point.lng)],
            map: mapRef.current,
            radius: newRadius,
            opacity: 0.9
          });
        });
        setHeatmapLayers(newLayers);
      } else {
        // Update radius of existing layers
        heatmapLayers.forEach((layer, index) => {
          const pointInfo = heatmapData[index].info;
          const newRadius = newRadiusData[pointInfo];
          if (newRadius) {
            layer.set('radius', newRadius);
          }
        });
      }
    }
  };
  

  const initHeatmap = (map) => {
    mapRef.current = map; // Store the map instance
    const google = window.google;
    const newHeatmapLayers = heatmapData.map(point => {
      const layer = new google.maps.visualization.HeatmapLayer({
        data: [new google.maps.LatLng(point.lat, point.lng)],
        map: map,
        radius: point.radius,
        opacity: 0.9
      });
      return layer;
    });
    setHeatmapLayers(newHeatmapLayers); // Store the created heatmap layers

    // Create a heatmap layer for each point
    heatmapData.forEach(point => {
      new google.maps.visualization.HeatmapLayer({
        data: [new google.maps.LatLng(point.lat, point.lng)],
        map: map,
        radius: point.radius,
        opacity: 0.9
      });
    });

    // Add click listener to the map
    map.addListener('click', (mapsMouseEvent) => {
      const clickedLocation = mapsMouseEvent.latLng;

      let closestPoint = null;
      let minDistance = Number.MAX_VALUE;

      heatmapData.forEach(point => {
        const distance = google.maps.geometry.spherical.computeDistanceBetween(
          new google.maps.LatLng(point.lat, point.lng),
          clickedLocation
        );
        if (distance < minDistance) {
          closestPoint = point;
          minDistance = distance;
        }
      });

      const threshold = 10000; // Adjust threshold distance as needed

      if (minDistance <= threshold) {
        setSelectedPoint(closestPoint);
      }
    });
  };

  const handleSendEmail = () => {
    // Make a GET request to the server's '/sendmail' endpoint
    fetch('/sendmail')
      .then(response => response.text())
      .then(data => alert('Email sent successfully!'))
      .catch(error => {
        console.error('Error sending email:', error);
        alert('Failed to send email.');
      });
  };

  // Function to determine the message based on the score range
  const getScoreMessage = (score) => {
    if (score  >=40) {
      return 'Danger Zone';
    } else if (score >= 20) {
      return 'Exercise Caution';
    } else {
      return 'Safe zone';
    }
  };

  const getScoreColor = (score) => {
    if (score  >=40) {
      return 'red';
    } else if (score >= 20) {
      return 'orange';
    } else {
      return 'green';
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>PROTEKT</h1>
      </header>
      <LoadScript
        const googleMapsApiKey = process.env.PrivateGKey; // Environmental Key to hide Google API
        libraries={["visualization", "geometry"]}
      >
        <GoogleMap
          mapContainerClassName="Map-container"
          center={center}
          zoom={11}
          onLoad={initHeatmap}
        >
          {selectedPoint && (
            <InfoWindow
              position={{ lat: selectedPoint.lat, lng: selectedPoint.lng }}
              onCloseClick={() => setSelectedPoint(null)}
            >
              <div>
                <h2>{selectedPoint.info}</h2>
                {/* Display crime data related to the selected point */}
                <h3 style={{ color: getScoreColor((scores)[selectedPoint.info])}}>
                <b>Score: {scores[selectedPoint.info]}</b><br></br>
                <b>{getScoreMessage(scores[selectedPoint.info])}</b>
                </h3>
                <p><b>Crime Count:</b> {crimeData[selectedPoint.info]?.crime_count}</p>
                <p><b>Most Common Crime:</b> {crimeData[selectedPoint.info]?.most_common_crime}</p>
              </div>
            </InfoWindow>
          )}
        </GoogleMap>
      </LoadScript>
      <footer className="App-footer" onClick={handleSendEmail}>
        Created by the AttachOnTech team
      </footer>
    </div>
  );
}

export default App;
