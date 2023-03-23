// TODO - Separate into multiple files

/**
 * MISC RELATED
 */

$(document).ready(function() {
    $('#action-list .nav-item').click(function(e) {
      e.preventDefault();
      $("#action-list .nav-item").removeClass("active");
      $("#action-list .nav-item .nav-link").removeClass("active");
      $($(this).children()[0]).addClass('active');

      $(".tab-pane").removeClass("active");
      $($(this.children[0]).attr('href')).addClass("active");
    });
  });
  

function replace_fa_icon(element, target_icon, replacement_icon, should_spin=false) {
    if (element.classList.contains(target_icon)) {
        element.classList.remove(target_icon);
        element.classList.add(replacement_icon);
        if (should_spin) {
            element.classList.add("fa-spin");
        }
    } else {
        element.children[0].classList.remove(target_icon);
        element.children[0].classList.add(replacement_icon);
        if (should_spin) {
            element.children[0].classList.add("fa-spin");
        }
    }
}


/***
 * JOBS RELATED
 */

// Add job from form data
$("#add_job_form").on("submit", function(){
    // Get form data from HTML form
    
    var url = '/run_job';
    var data = {
        'job_name': $("#job_name").val(),
        'image': $("#job_image").val(),
    };

    $.ajax({
        url: url,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function (data) {
            window.alert("Job " + data.job_name + " has been started");
            window.location.reload();
        }
    });
    return false;
});


// Runs job again based on image_id and job_name
function run_job(job_name, image_id) {
    replace_fa_icon(window.event.target, "fa-redo", "fa-spinner", true);
    var url = '/run_job';
    var data = {
        'job_name': job_name.substring(0, job_name.length-9), // Remove last 9 characters from the job name
        'image': image_id
    };

    $.ajax({
        url: url,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function (data) {
            window.alert("Job " + data.job_name + " has been started");
            window.location.reload();
        }
    });
}

// Removes job based on job_name
function remove_job(job_name, retry_as_service=true) {
    replace_fa_icon(window.event.target, "fa-trash", "fa-spinner", true);
    const thiz = this;
    var url = '/remove_job';
    var data = {
        'job_name': job_name
    };

    $.ajax({
        url: url,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function (data) {
            window.alert("Job " + data.job_name + " has been removed");
            window.location.reload();
        },
        error: function () {
            if (retry_as_service) {
                thiz.remove_service(job_name, false);
            } else {
                window.alert("Service or Job " + job_name + " could not be removed");
                window.location.reload();
            }
        }
    });
}

/***
 * SERVICES RELATED
 */


// Add job from form data
$("#add_service_form").on("submit", function(){
    // Get form data from HTML form
    var url = '/add_service';
    var data = {
        'service_name': $("#service_name").val(),
        'image': $("#service_image").val(),
    };

    console.log(data);

    $.ajax({
        url: url,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function (data) {
            window.alert("Service " + data.service_name + " has been started");
            window.location.reload();
        }
    });
    return false;
});

// Updates a service's replicas
function update_replicas(service_name, replicas) {
    var url = '/scale_service';
    var data = {
        'service_name': service_name,
        'replicas': replicas
    };

    $.ajax({
        url: url,
        type: 'PUT',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function (data) {
            window.alert("Service " + data.service_name + " has been updated with " + data.replicas + " replicas.");
            window.location.reload();
        }
    });
}

function remove_service(service_name, retry_as_job=true) {
    replace_fa_icon(window.event.target, "fa-trash", "fa-spinner", true);
    const thiz = this;
    var url = '/remove_service';
    var data = {
        'service_name': service_name
    };

    $.ajax({
        url: url,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function (data) {
            window.alert("Service " + data.service_name + " has been removed");
            window.location.reload();
        },
        error: function () {
            if (retry_as_job) {
                thiz.remove_job(service_name, false);
            } else {
                window.alert("Service or Job " + service_name + " could not be removed");
                window.location.reload();
            }
        }
    });
}

/**
 * IMAGES RELATED
 */

// Add image from form data
$("#add_image_form").on("submit", function(){
    // Get form data from HTML form
    var url = '/add_image';
    var data = {
        'image_name': $("#add_image_name").val(),
        'image_version': $("#add_image_version").val() || "",
    };

    console.log(data)

    $.ajax({
        url: url,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function (data) {
            window.alert(`Image ${data.image} has been added.`);
            window.location.reload();
        }
    });
    return false;
});

// Removes image from form data
$("#remove_image_form").on("submit", function(){
    // Get form data from HTML form
    var url = '/remove_image';
    var data = {
        'image_name': $("#remove_image_name").val()
    };

    $.ajax({
        url: url,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function (data) {
            window.alert(data.message);
            window.location.reload();
        },
        error: function (data) {
            window.alert(data.responseJSON.message);
        }
    });
    return false;
});