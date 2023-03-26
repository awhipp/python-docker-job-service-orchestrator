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
    if (target_icon === 'text') {
        if (should_spin) {
            $(element).html(`<i class="fas ${replacement_icon} fa-spin"></i>`)
        } else {
            $(element).html(`<i class="fas ${replacement_icon}"></i>`)
        }
    }else if (element.classList.contains(target_icon)) {
        element.classList.remove(target_icon);
        element.classList.add(replacement_icon);
        if (should_spin) {
            element.classList.add("fa-spin");
        } else {
            element.classList.remove("fa-spin");
        }
    } else {
        element.children[0].classList.remove(target_icon);
        element.children[0].classList.add(replacement_icon);
        if (should_spin) {
            element.children[0].classList.add("fa-spin");
        } else {
            element.children[0].classList.remove("fa-spin");
        }
    }
}


/***
 * JOBS RELATED
 */

// Add job from form data
$("#add_job_form").on("submit", function(){
    replace_fa_icon($("#add_job_form button[type='submit']"), "text", "fa-spinner", true);
    
    var url = '/jobs/run';
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
    var url = '/jobs/run';
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
    var url = '/jobs/remove';
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

function get_job_logs(job_name) {
    let eventTarget = window.event.target;
    replace_fa_icon(eventTarget, "fa-file-alt", "fa-spinner", true);
    var url = '/jobs/logs';
    var data = {
        'job_name': job_name
    };

    $.ajax({
        url: url,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function (data) {
            showModal(`Job: ${data.job_name} Logs`, data.logs);
            replace_fa_icon(eventTarget, "fa-spinner", "fa-file-alt", false);
        }
    });
}
/***
 * SERVICES RELATED
 */


// Add job from form data
$("#add_service_form").on("submit", function(){
    replace_fa_icon($("#add_service_form button[type='submit']"), "text", "fa-spinner", true);

    var url = '/services/add';
    var data = {
        'service_name': $("#service_name").val(),
        'image': $("#service_image").val(),
    };

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
    var url = '/services/scale';
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
    var url = '/services/remove';
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

function get_service_logs(service_name) {
    let eventTarget = window.event.target;
    replace_fa_icon(eventTarget, "fa-file-alt", "fa-spinner", true);
    var url = '/services/logs/';
    var data = {
        'service_name': service_name
    };

    $.ajax({
        url: url,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function (data) {
            showModal(`Service: ${data.service_name} Logs`, data.logs);
            replace_fa_icon(eventTarget, "fa-spinner", "fa-file-alt", false);
        }
    });
}

/**
 * IMAGES RELATED
 */

// Add image from form data
$("#add_image_form").on("submit", function(){
    replace_fa_icon($("#add_image_form button[type='submit']"), "text", "fa-spinner", true);

    var url = '/images/add';
    var data = {
        'image_name': $("#add_image_name").val(),
        'image_version': $("#add_image_version").val() || "",
    };

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
    replace_fa_icon($("#remove_image_form button[type='submit']"), "text", "fa-spinner", true);
    
    var url = '/images/remove';
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

/**
 * Open Modal
 */
function showModal(title, text) {
    // Get a reference to the modal element
    const modal = document.getElementById('log_modal');

    // Get a reference to the modal's title element
    const modalTitle = modal.querySelector('.modal-title');
    modalTitle.innerText = title;
  
    // Get a reference to the modal's text element
    const modalText = modal.querySelector('.modal-body p');
  
    // Set the text of the modal's text element
    modalText.innerText = text;
  
    // Show the modal
    $(modal).modal('show')

    $('.close_log_modal').on('click', function() {
        $(modal).modal('hide');
    });
    
    setTimeout(function() {
        var maxScrollHeight = $(".modal-body")[0].scrollHeight - $(".modal-body").outerHeight();

        $(".modal-body").scrollTop(maxScrollHeight);
    }, 500);
}

function refresh_logs() {
    let eventTarget = window.event.target;
    replace_fa_icon(eventTarget, "fa-redo", "fa-spinner", true);

    modal_title = $(".modal .modal-title").text();
    route = '';
    payload = {};

    if (modal_title.includes("Service")) {
        service_name = modal_title.substring(9, modal_title.length-5);
        route = '/services/logs';
        payload = {
            'service_name': service_name
        }
    } else if (modal_title.includes("Job")) {
        job_name = modal_title.substring(5, modal_title.length-5);
        route = '/jobs/logs';
        payload = {
            'job_name': job_name
        }
    }

    var url = route;
    var data = payload;

    $.ajax({
        url: url,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function (data) {
            if ('job_name' in data) {
                showModal(`Job: ${data.job_name} Logs`, data.logs);
            } else if ('service_name' in data) {
                showModal(`Service: ${data.service_name} Logs`, data.logs);
            }
            replace_fa_icon(eventTarget, "fa-spinner", "fa-redo", false);
        }
    });
}

