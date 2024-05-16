  const song = document.querySelector(".song");
  const play = document.querySelector(".play");
  const replay = document.querySelector(".replay");
  const outline = document.querySelector(".moving-outline circle");
  const video = document.querySelector(".vid-container video");
  //Sounds
  const sounds = document.querySelectorAll(".sound-picker button");
  //Time Display
  const timeDisplay = document.querySelector(".time-display");
  const outlineLength = outline.getTotalLength();
  //Duration
  const timeSelect = document.querySelectorAll(".time-select button");
  let fakeDuration = 10;
  let initialFakeDuration = fakeDuration; // Store the initial fake duration

  outline.style.strokeDashoffset = outlineLength;
  outline.style.strokeDasharray = outlineLength;
  timeDisplay.textContent = `${Math.floor(fakeDuration / 60)}:${Math.floor(
    fakeDuration % 60
  )}`;

  sounds.forEach((sound) => {
    sound.addEventListener("click", function () {
      song.src = this.getAttribute("data-sound");
      video.src = this.getAttribute("data-video");
      checkPlaying(song);
    });
  });

  play.addEventListener("click", function () {
    checkPlaying(song);
  });

  replay.addEventListener("click", function () {
    fakeDuration = initialFakeDuration;
    restartSong(song);
  });

  const restartSong = (song) => {
    let currentTime = song.currentTime;
    song.currentTime = 0;
    console.log("Restarted song");
  };

  timeSelect.forEach((option) => {
    option.addEventListener("click", function () {
      fakeDuration = this.getAttribute("data-time");
      timeDisplay.textContent = `${Math.floor(fakeDuration / 60)}:${Math.floor(
        fakeDuration % 60
      )}`;
    });
  });

  const checkPlaying = (song) => {
    if (song.paused) {
      song.play();
      video.play();
      // play.src = "./svg/pause.svg";
    } else {
      song.pause();
      video.pause();
      // play.src = "./svg/play.svg";
    }
  };

  replay.addEventListener("click", function () {
    fakeDuration = initialFakeDuration; // Reset the fake duration
    restartSong(song);
  });

  const playVideo = () => {
    video.play();
  };

  song.ontimeupdate = function () {
    let currentTime = song.currentTime;
    let elapsed = fakeDuration - currentTime;
    let reverse = currentTime - fakeDuration;
    let seconds = Math.floor(elapsed % 60);
    let minutes = Math.floor(elapsed / 60);
    timeDisplay.textContent = `${minutes}:${seconds}`;
    let progress = outlineLength - (currentTime / fakeDuration) * outlineLength;
    outline.style.strokeDashoffset = progress;

    if (currentTime >= fakeDuration) {
      song.pause();
      // song.currentTime = 0;
      play.src = "./svg/play.svg";
      video.pause();
    } else if (currentTime >= song.duration) {
      if (song.duration < fakeDuration) {
        song.currentTime = 0;
        song.play();
      } else {
        song.pause();
        play.src = "./svg/play.svg";
        video.pause();
      }
    }
  };

  const startTimer = () => {
    let timerInput = document.getElementById("timerInput");
    let timer = parseInt(timerInput.value, 10);

    if (isNaN(timer) || timer <= 0) {
      alert("Please enter a positive integer value for the timer.");
      return;
    }

    if (timer >= fakeDuration) {
      let repetitions = Math.floor(timer / fakeDuration);
      let remainingTime = timer % fakeDuration;

      for (let i = 0; i < repetitions; i++) {
        playVideo();
        video.addEventListener("ended", playVideo);
      }

      if (remainingTime > 0) {
        setTimeout(function () {
          stopVideo();
          alert("Timer ended!");
        }, remainingTime * 1000);
      } else {
        alert("Timer ended!");
      }
    } else {
      setTimeout(function () {
        stopVideo();
        alert("Timer ended!");
      }, timer * 100);
    }
  };

  const stopVideo = () => {
    video.pause();
    video.currentTime = 0;
  };

  replay.addEventListener("click", startTimer);
