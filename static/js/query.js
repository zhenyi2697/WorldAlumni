/*
 * Query user's locatio and nearby schoolmates
 *
 * copyright zhenyi2697
 * Updated 04/20/2014
 *
*/


  // use html 5 to load location
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showLocation, showLocationError);
  } else {
    loadErrorMessage("Sorry, Geolocation is not supported by your browser, maybe you could consider using a more advanced one ;)");
  }

  var current_latitude;
  var current_longitude;
  function showLocation(location) {
      current_latitude = location.coords.latitude;
      current_longitude = location.coords.longitude;
      $("#latitude").html(current_latitude);
      $("#longitude").html(current_longitude);

      $("#current-location").show();
      $(".find-friend-div").show();
      $("#location-error-message").hide();
      $("#loading-message").hide();
  }

  function loadErrorMessage(message) {
    $("#location-error-message").html(message);
    $("#location-error-message").show();
  }

  function showLocationError(error) {

    var message = ""
    switch(error.code) {
      case error.PERMISSION_DENIED:
        message = "Sorry, we cannot give your nearby friends without knowing your location -_- ...";
        break;
      case error.POSITION_UNAVAILABLE:
        message = "Sorry, we cannot get your current location, try refresh the page ;)";
        break;
      case error.TIMEOUT:
        message = "Location request timedout, retry please ;)";
        break;
      case error.UNKNOWN_ERROR:
        message = "Somethings wierd happens, refresh page please ;)"
        break;
    }
    loadErrorMessage(message);
    $("#current-location").hide();
    $("#loading-message").hide();
  }

  var mapOpened = false;
  var mapInitiated = false;
  var toggleMap = function(){
    if(mapOpened) {
      $("#friend-map").slideUp();
      mapOpened = false;
      $("#showMap").html("<i class='fa fa-search'></i> open map");
    }else {
      $("#friend-map").slideDown(function(){
        if (!mapInitiated) {
          initMap();
          mapInitiated = true;
          refreshMap();
        }
      });
      mapOpened = true;
      $("#showMap").html("<i class='fa fa-search'></i> close map");
    }
  }

  var markers = [];
  var load_friends = function(friends){

    var rows = [];
    var row_data = "";
    var f;
    var context_data = "";

    if (friends.length <= 1) {
      $("#friend-message").html("It seems that you are the only one around here, come back later!");
    } else {
      var html = "We have found "+ (friends.length - 1) +" schoolmates for you";
      html += "<span class='label label-warning text-small' id='showMap' onclick='toggleMap();' style='margin-left:10px;cursor:pointer;'><i class='fa fa-search'></i> open map</span>"
      $("#friend-message").html(html);
    }


    for (var i = 0; i < friends.length; i++) {
      f = friends[i];
      row_data = "<tr>";
      if (f.provider == 'facebook') {
        row_data += "<td><img src='"+ f.image_url +"?width=40&height=40' style='width:24px;height:24px;' alt='"+f.first_name+"' class='img-circle friend-thumbnail'/></td>";
        row_data += "<td><a href='http://www.facebook.com/"+ f.uid  +"' target='_blank'>"+ f.first_name + " "+ f.last_name +"</a></td>";
        context_data = "<img src='"+ f.image_url +"?width=24&height=24' style='width:24px;height:24px;margin-right:5px;' class='img-circle friend-thumbnail' style='margin-right:5px;'/><a href='http://www.facebook.com/"+ f.uid  +"' target='_blank'>" + f.first_name + " " + f.last_name + "</a>";
      } else {
        row_data += "<td><img src='"+ f.image_url + "' style='width:40px;height:40px;' class='img-circle friend-thumbnail' /></td>";
        row_data += "<td>"+ f.first_name + " "+ f.last_name +"</td>";
        context_data = "<img src='"+ f.image_url + "' style='width:24px;height:24px;margin-right:5px;' class='img-circle friend-thumbnail'/>" + f.first_name + " " + f.last_name;
      }

      if (f.associated_attendances.length > 0 && f.attendances.length > 0 ) {
        row_data += "<td>" +f.associated_attendances[0].school + "</td>";
      } else {
        row_data += "<td></td>";
      }

      row_data += "<td class='hidden-xs'>"+ f.distance +"</td>";
      row_data += "<td class='hidden-xs'>"+ f.appear_time +"</td>";
      row_data += "<td class='visible-xs'>"+ f.distance +" ("+ f.appear_time +")</td>";

      rows.push(row_data);

      //gps data
      if (f.latitude != "0" && f.longitude != "0"){
        var gpsdata = {
          data: context_data,
          latLng: [f.latitude, f.longitude],
          id: f.bindingId
        }
        markers.push(gpsdata);
      }

    }
    var html = rows.join();
    $("#friend-table").html(html);

    if (mapInitiated) {
      refreshMap();
    }

  }

  var initMap = function(){
    $("#friend-map").gmap3({
	    map:{
	      options:{
	        center:[current_latitude, current_longitude],
	        zoom:12
	      }
	    }
    });
  }

  var refreshMap = function(){

    // clear old markers
	  $("#friend-map").gmap3({
	  	clear:{name:"marker"}
	  });

    // init new markers
    $("#friend-map").gmap3({
        marker: {
            values: markers,
	          events:{
	            click: function(marker, event, context){
	            	var map = this.gmap3("get"),
	  	          infowindow = this.gmap3({get:{name:"infowindow"}});
	  	          if (infowindow){
	  	            infowindow.close();
	  	            infowindow.setContent(context.data);
	  	            infowindow.open(map, marker);
	  	          } else {
	  	            this.gmap3({
	  	              infowindow:{
	  	                anchor:marker,
	  	                options:{content: context.data }
	  	              }
	  	            });
	  	          }
	            }
	          }
        }
    });
  
  }
  
  var user_nearby = function(){

    post_params = {
      'bindingId': bindingId,
      'longitude': current_longitude,
      'latitude': current_latitude
    }

    $.post('/api/nearby_users/', post_params).done(function(d){
      console.log(d);
      $("#sent_result").html("Your location has been sent to server")
      load_friends(d);
    }, 'json');

  }

  var updateSetting = function(entryId){

    var value = 0;
    if (entryId == 1) {

      if($("#distance_only_input").is(':checked') ) {
        value = 1;
      } else {
        value = 0;
      }

    } else if (entryId == 2) {

      if( $("#invisible_input").is(':checked') ) {
        value = 1;
      } else {
        value = 0;
      }

    }

    post_params = {
      'bindingId': bindingId,
      'entryId': entryId,
      'value': value
    }

    $.post('/api/'+bindingId+'/settings/', post_params).done(function(d){
      console.log(d);
    }, 'json');

  }

