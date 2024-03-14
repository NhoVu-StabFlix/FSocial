$(document).ready(function () {
    $("#post-form").submit(function (e) {

        e.preventDefault();
        let post_caption = $("#post-caption").val();
        let post_visibility = $("#visibility").val();
        let image_input = $("#post-thumbnail")[0];
        let image = image_input.files[0];
        let image_name = image.name
        console.log(post_caption);
        console.log(image_name);
        console.log(post_visibility);
        let formData = new FormData();
        formData.append("post-caption", post_caption);
        formData.append("post-thumbnail", image);
        formData.append("visibility", post_visibility);
        $.ajax({
            url: "/create-post",
            method: "POST",
            data: formData,
            headers: {
                'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
            },
            contentType: false,
            processData: false,

            success: function (data) {
                console.log(data);
            },
            error: function (error) {
                console.log(error);
            }


        })
    })

})