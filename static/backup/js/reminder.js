
	var reminderTimeoutId;

function fetchData() 


{
	var taskname = document.getElementById('task').value;
	var taskdetails = document.getElementById('taskdetails').value;
	var tasktime = document.getElementById('tasktime').value;
    var timeArray = tasktime.split(':');
	
	var hours = parseInt(timeArray[0]).toString().padStart(2, '0');
  	var minutes = parseInt(timeArray[1]).toString().padStart(2, '0');
  	var seconds = parseInt(timeArray[2]).toString().padStart(2, '0');
    var settime = new Date();
  		settime.setHours(parseInt(hours));
  		settime.setMinutes(parseInt(minutes));
  		settime.setSeconds(parseInt(seconds));
  
  		document.getElementById('test').textContent = settime;
  
  	var currentTime = new Date();
  	var timeDifference = settime.getTime() - currentTime.getTime();
  		document.getElementById('test2').textContent = currentTime;
  		if (timeDifference <= 0) {
				timeDifference += 24 * 60 * 60 * 1000;
								}

    // set the timeout for this reminder
    var reminderTimeoutId = setTimeout(playReminder, timeDifference);
 		reminderTimeoutIds.push(reminderTimeoutId);
  }


  
		
	function playReminder(){
		var audio1 = document.getElementById('audio');
		audio1.play();

	}

// ----------------------------------------------------------------------
// var reminderTimeoutIds = []; // array to store the timeout IDs for each reminder

// function fetchData() {
//   // get all the tasktime elements from the page
//   var tasktimes = document.querySelectorAll('[id^="tasktime"]');

//   // loop through all the tasktimes
//   for (var i = 0; i < tasktimes.length; i++) {
//     var tasktime = tasktimes[i].value;
//     var timeArray = tasktime.split(':');
//     var hours = timeArray[0].padStart(2, '0');
//     var minutes = timeArray[1].padStart(2, '0');
//     var seconds = timeArray[2].padStart(2, '0');

//     var settime = new Date();
//     settime.setHours(hours);
//     settime.setMinutes(minutes);
//     settime.setSeconds(seconds);

//     var currentTime = new Date();
//     var timeDifference = settime.getTime() - currentTime.getTime();

//     // if the time has already passed for this reminder, skip it
//     if (timeDifference <= 0) {
//       continue;
//     }

//     // set the timeout for this reminder
//     var reminderTimeoutId = setTimeout(playReminder, timeDifference);
//     reminderTimeoutIds.push(reminderTimeoutId);
//   }
// }

// function playReminder() {
//   // play the reminder sound or show a reminder popup
//   // ...
  
//   // clear the timeout for this reminder
//   clearTimeout(reminderTimeoutIds.shift()); // remove the first item from the array
// }
// // ----------------------------------------------------------------------





