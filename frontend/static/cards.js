// cards.js

// Функция для создания карточки погоды
function createWeatherCard(location) {
    const card = document.createElement('div');
    card.className = 'col-12 col-lg-3 col-md-6 mb-4';

    card.innerHTML = `
        <div class="card h-100 position-relative weather-card">
            <div class="position-absolute weather-card-delete-form">
                <button class="btn-close" onclick="deleteLocation('${location.name}', ${location.latitude}, ${location.longitude})" aria-label="Delete"></button>
            </div>
            <img class="card-img-top img-fluid"
                 src="https://openweathermap.org/img/wn/${getWeatherIcon(location.main_weather)}@4x.png"
                 alt="Weather icon">
            <div class="card-body d-flex flex-column">
                <h1 class="card-text">${location.temperature}°C</h1>
                <h3 class="card-title">${location.name}, ${location.country}</h3>
                <p class="card-text mb-1">${location.main_weather}</p>
                <p class="card-text mb-1">Feels like <span>${location.temperature_feels}</span>°C.</p>
                <p class="card-text mb-1">Humidity: ${location.humidity}%</p>
                <p class="card-text mb-1">Wind speed: ${location.wind_speed} m/s</p>
            </div>
        </div>
    `;

    return card;
}

// Функция для определения иконки погоды
function getWeatherIcon(mainWeather) {
    const icons = {
        'Clear': '01n',
        'Clouds': '04n',
        'Snow': '13n',
        'Rain': '10n',
        'Drizzle': '09n',
        'Thunderstorm': '11n',
        'Mist': '50n',
        'default': '01n'
    };

    return icons[mainWeather] || icons['default'];
}

// Функция для создания карточки локации
function createLocationCard(location) {
    const card = document.createElement('div');
    card.className = 'col-12 col-lg-3 col-md-6 mb-4';

    card.innerHTML = `
        <div class="card h-100">
            <div class="card-body d-flex flex-column">
                <h5 class="card-title">${location.name}</h5>
                <p class="card-text mb-1">Latitude: ${location.lat}</p>
                <p class="card-text mb-1">Longitude: ${location.lon}</p>
                <p class="card-text mb-1">Country: ${location.country || 'N/A'}</p>
                <p class="card-text mb-3">State: ${location.state || 'N/A'}</p>
                <div class="mt-auto">
                    <button class="btn btn-primary w-100" onclick="addLocation('${location.name}', ${location.lat}, ${location.lon})">Add</button>
                </div>
            </div>
        </div>
    `;

    return card;
}