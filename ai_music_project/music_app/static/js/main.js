// Main JavaScript for AI Music Generator
document.addEventListener('DOMContentLoaded', function() {
    // Initialize elements
    initializeUI();
    
    // Initialize tabs
    const triggerTabList = document.querySelectorAll('#generationTabs button');
    triggerTabList.forEach(triggerEl => {
        const tabTrigger = new bootstrap.Tab(triggerEl);
        triggerEl.addEventListener('click', event => {
            event.preventDefault();
            tabTrigger.show();
        });
    });
    
    // Initialize tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    
    // Initialize genre selection
    const genreCards = document.querySelectorAll('.genre-card');
    genreCards.forEach(card => {
        card.addEventListener('click', function() {
            // Remove selected class from all cards
            genreCards.forEach(c => c.classList.remove('selected'));
            // Add selected class to clicked card
            this.classList.add('selected');
            // Set hidden input value
            document.getElementById('selectedGenre').value = this.dataset.genre;
        });
    });
    
    // Initialize range sliders
    initRangeSliders();
    
    // Setup Video Upload
    setupVideoUpload();
    
    // Setup form submission
    setupFormSubmission();
    
    // Initialize waveform if wavesurfer.js is available
    if (typeof WaveSurfer !== 'undefined') {
        initializeWaveform();
    }
});

function initializeUI() {
    // Update values on page load
    document.querySelectorAll('input[type="range"]').forEach(range => {
        const valueDisplay = document.getElementById(range.id + 'Value');
        if (valueDisplay) {
            if (range.id === 'length') {
                valueDisplay.textContent = range.value + ' seconds';
            } else if (range.id === 'tempo') {
                valueDisplay.textContent = range.value + ' BPM';
            } else {
                valueDisplay.textContent = range.value;
            }
        }
    });
    
    // Set default tab
    const firstTab = document.querySelector('#generationTabs button:first-child');
    if (firstTab) {
        firstTab.classList.add('active');
    }
    
    // Set default genre
    const defaultGenre = document.querySelector('.genre-card[data-genre="electronic"]');
    if (defaultGenre) {
        defaultGenre.classList.add('selected');
        document.getElementById('selectedGenre').value = defaultGenre.dataset.genre;
    }
}

function initRangeSliders() {
    // Add listeners to range inputs to update value displays
    document.querySelectorAll('input[type="range"]').forEach(range => {
        const valueDisplay = document.getElementById(range.id + 'Value');
        if (valueDisplay) {
            range.addEventListener('input', function() {
                if (this.id === 'length') {
                    valueDisplay.textContent = this.value + ' seconds';
                } else if (this.id === 'tempo') {
                    valueDisplay.textContent = this.value + ' BPM';
                } else {
                    valueDisplay.textContent = this.value;
                }
            });
        }
    });
}

function setupVideoUpload() {
    const uploadZone = document.getElementById('videoUploadZone');
    const fileInput = document.getElementById('videoFile');
    const videoPreviewContainer = document.getElementById('videoPreviewContainer');
    const videoPreview = document.getElementById('videoPreview');
    const uploadProgress = document.getElementById('uploadProgress');
    const uploadProgressBar = document.getElementById('uploadProgressBar');
    const videoFileNameEl = document.getElementById('videoFileName');
    const removeVideoBtn = document.getElementById('removeVideoBtn');
    
    if (!uploadZone || !fileInput) return;
    
    // Click on upload zone triggers file input
    uploadZone.addEventListener('click', () => {
        fileInput.click();
    });
    
    // Handle drag and drop
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadZone.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    ['dragenter', 'dragover'].forEach(eventName => {
        uploadZone.addEventListener(eventName, () => {
            uploadZone.classList.add('drag-over');
        }, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        uploadZone.addEventListener(eventName, () => {
            uploadZone.classList.remove('drag-over');
        }, false);
    });
    
    // Handle dropped files
    uploadZone.addEventListener('drop', (e) => {
        const files = e.dataTransfer.files;
        if (files.length) {
            fileInput.files = files;
            handleVideoFile(files[0]);
        }
    });
    
    // Handle selected files
    fileInput.addEventListener('change', () => {
        if (fileInput.files.length) {
            handleVideoFile(fileInput.files[0]);
        }
    });
    
    // Handle video file selection
    function handleVideoFile(file) {
        // Check if it's a video file
        if (!file.type.match('video/*')) {
            showAlert('Please select a valid video file', 'danger');
            return;
        }
        
        // Display file name
        if (videoFileNameEl) {
            videoFileNameEl.textContent = file.name;
        }
        
        // Show progress (simulated for this demo)
        if (uploadProgress) {
            uploadProgress.style.display = 'block';
            simulateUploadProgress();
        }
        
        // Create video preview
        const videoURL = URL.createObjectURL(file);
        if (videoPreview) {
            videoPreview.src = videoURL;
            videoPreview.onloadedmetadata = () => {
                videoPreviewContainer.style.display = 'block';
                uploadZone.style.display = 'none';
                
                // Update length slider based on video duration if needed
                const lengthSlider = document.getElementById('length');
                if (lengthSlider && videoPreview.duration) {
                    const duration = Math.min(Math.round(videoPreview.duration), 180);
                    lengthSlider.value = duration;
                    document.getElementById('lengthValue').textContent = duration + ' seconds';
                }
            };
        }
        
        // Enable remove button
        if (removeVideoBtn) {
            removeVideoBtn.style.display = 'block';
            removeVideoBtn.addEventListener('click', removeVideo);
        }
    }
    
    // Simulate upload progress (for demonstration)
    function simulateUploadProgress() {
        let progress = 0;
        const interval = setInterval(() => {
            progress += 5;
            uploadProgressBar.style.width = progress + '%';
            uploadProgressBar.setAttribute('aria-valuenow', progress);
            
            if (progress >= 100) {
                clearInterval(interval);
                uploadProgress.style.display = 'none';
            }
        }, 100);
    }
    
    // Remove uploaded video
    function removeVideo() {
        fileInput.value = '';
        videoPreview.src = '';
        videoPreviewContainer.style.display = 'none';
        uploadZone.style.display = 'block';
        if (videoFileNameEl) {
            videoFileNameEl.textContent = '';
        }
        if (removeVideoBtn) {
            removeVideoBtn.style.display = 'none';
        }
    }
}

function setupFormSubmission() {
    const form = document.getElementById('generationForm');
    const resultsSection = document.getElementById('resultsSection');
    const loadingSection = document.getElementById('loadingSection');
    
    if (!form) return;
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Validate form
        const selectedGenre = document.getElementById('selectedGenre').value;
        if (!selectedGenre) {
            showAlert('Please select a genre', 'warning');
            return;
        }
        
        // Show loading section
        if (loadingSection) {
            loadingSection.style.display = 'block';
            
            // Scroll to loading section
            loadingSection.scrollIntoView({ behavior: 'smooth' });
        }
        
        // Simulate AI processing (for demonstration)
        setTimeout(() => {
            if (loadingSection) {
                loadingSection.style.display = 'none';
            }
            
            // Show results section
            if (resultsSection) {
                resultsSection.style.display = 'block';
                
                // Scroll to results
                resultsSection.scrollIntoView({ behavior: 'smooth' });
                
                // Add audio source (for demonstration)
                const audioPlayer = document.getElementById('musicPlayer');
                if (audioPlayer) {
                    // In a real app, this would be the URL of the generated audio
                    // For demo, we use a placeholder
                    audioPlayer.src = 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3';
                    
                    // Update waveform if available
                    if (window.wavesurfer) {
                        window.wavesurfer.load(audioPlayer.src);
                    }
                }
                
                // Update music info
                updateMusicInfo();
            }
        }, 3000); // Simulate 3 seconds of processing time
        
        // In a real application, you would send the form data to the server here
        // const formData = new FormData(form);
        // fetch('/generate-music/', {
        //     method: 'POST',
        //     body: formData
        // })
        // .then(response => response.json())
        // .then(data => {
        //     // Handle response
        // })
        // .catch(error => {
        //     console.error('Error:', error);
        // });
    });
}

function initializeWaveform() {
    // Initialize WaveSurfer for audio visualization
    window.wavesurfer = WaveSurfer.create({
        container: '#waveform',
        waveColor: 'rgba(187, 134, 252, 0.3)',
        progressColor: 'rgba(187, 134, 252, 0.8)',
        cursorColor: '#03dac6',
        barWidth: 2,
        barRadius: 3,
        cursorWidth: 1,
        height: 80,
        barGap: 3,
        responsive: true
    });
    
    // Connect play button to audio element
    document.getElementById('playBtn').addEventListener('click', function() {
        const audioPlayer = document.getElementById('musicPlayer');
        if (audioPlayer.paused) {
            audioPlayer.play();
            this.innerHTML = '<i class="bi bi-pause-fill"></i>';
        } else {
            audioPlayer.pause();
            this.innerHTML = '<i class="bi bi-play-fill"></i>';
        }
    });
    
    // Connect wavesurfer to audio element
    document.getElementById('musicPlayer').addEventListener('play', function() {
        window.wavesurfer.play();
        document.getElementById('playBtn').innerHTML = '<i class="bi bi-pause-fill"></i>';
    });
    
    document.getElementById('musicPlayer').addEventListener('pause', function() {
        window.wavesurfer.pause();
        document.getElementById('playBtn').innerHTML = '<i class="bi bi-play-fill"></i>';
    });
    
    // Update current time
    window.wavesurfer.on('audioprocess', function() {
        const currentTime = window.wavesurfer.getCurrentTime();
        document.getElementById('currentTime').textContent = formatTime(currentTime);
    });
    
    window.wavesurfer.on('ready', function() {
        const duration = window.wavesurfer.getDuration();
        document.getElementById('duration').textContent = formatTime(duration);
    });
    
    // Enable seeking
    window.wavesurfer.on('seek', function(position) {
        const audioPlayer = document.getElementById('musicPlayer');
        audioPlayer.currentTime = position * audioPlayer.duration;
    });
}

function updateMusicInfo() {
    // Get form values
    const genre = document.querySelector('.genre-card.selected')?.dataset.genre || 'electronic';
    const tempo = document.getElementById('tempo').value;
    const length = document.getElementById('length').value;
    const vocals = document.getElementById('includeVocals').checked ? 'Yes' : 'No';
    
    // Update info in results section
    document.getElementById('resultGenre').textContent = capitalizeFirstLetter(genre);
    document.getElementById('resultTempo').textContent = tempo + ' BPM';
    document.getElementById('resultLength').textContent = length + ' seconds';
    document.getElementById('resultVocals').textContent = vocals;
    
    // Update timestamp
    document.getElementById('generationTime').textContent = new Date().toLocaleString();
}

// Helper Functions
function showAlert(message, type = 'info') {
    const alertsContainer = document.getElementById('alertsContainer');
    if (!alertsContainer) return;
    
    const alertEl = document.createElement('div');
    alertEl.className = `alert alert-${type} alert-dismissible fade show`;
    alertEl.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    alertsContainer.appendChild(alertEl);
    
    // Auto dismiss after 5 seconds
    setTimeout(() => {
        alertEl.classList.remove('show');
        setTimeout(() => alertEl.remove(), 300);
    }, 5000);
}

function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${minutes}:${secs < 10 ? '0' : ''}${secs}`;
}

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
} 