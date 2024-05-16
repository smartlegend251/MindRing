const dropzone = document.getElementById('dropzone');
		const videoPreview = document.getElementById('video-preview');

		// Prevent default drag behaviors
		['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
		  dropzone.addEventListener(eventName, preventDefaults, false)
		  document.body.addEventListener(eventName, preventDefaults, false)
		});

		// Highlight drop zone when item is dragged over
		['dragenter', 'dragover'].forEach(eventName => {
		  dropzone.addEventListener(eventName, highlightDropzone, false)
		});

		// Remove highlight when item is dragged away
		['dragleave', 'drop'].forEach(eventName => {
		  dropzone.addEventListener(eventName, unhighlightDropzone, false)
		});

		// Handle dropped items
		dropzone.addEventListener('drop', handleDrop, false)

		function preventDefaults (e) {
		  e.preventDefault()
		  e.stopPropagation()
		}

		function highlightDropzone() {
			dropzone.classList.add('active');
		}

		function unhighlightDropzone() {
			dropzone.classList.remove('active');
		}

		function handleDrop(e) {
			const files = e.dataTransfer.files;
			if (files.length > 0) {
				const videoFile = files[0];
				const videoUrl = URL.createObjectURL(videoFile);
				videoPreview.src = videoUrl;
				videoPreview.style.display = 'block';
				dropzone.style.display = 'none';
			}
		}






    function handleFileSelect(event) {
      var files = event.target.files; // Get the selected files
      
      // Iterate through each file and perform necessary actions
      for (var i = 0; i < files.length; i++) {
        var file = files[i];
        
        // Display file information (optional)
        console.log("File name: " + file.name);
        console.log("File type: " + file.type);
        console.log("File size: " + file.size + " bytes");
        console.log("-----------------------------");
        
        // Perform additional actions here (e.g., upload file to a server)
        // ...
      }
    }
  


		