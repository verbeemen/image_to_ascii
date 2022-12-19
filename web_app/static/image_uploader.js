//////////////////////////////////
// Drag and Drop image uploader //
//////////////////////////////////


/**
 *
 * Drag and Drop image uploader
 *
 */
!(function (e) {
    /**
      * Copyright (c) 2019 Christian Bayer; Licensed MIT 
      * extended for image click event
      */
    e.fn.imageUploader = function (t) {
        let n,
            i = {
                preloaded: [],
                imagesInputName: "images",
                preloadedInputName: "preloaded",
                label: "Drag & Drop files here or click to browse",
                extensions: [".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"],
                mimes: ["image/jpeg", "image/png"],
                maxSize: void 0,
                maxFiles: void 0,
            },
            a = this,
            s = new DataTransfer();
        (a.settings = {}),
            (a.init = function () {
                (a.settings = e.extend(a.settings, i, t)),
                    a.each(function (t, n) {
                        let i = o();
                        if ((e(n).append(i), i.on("dragover", r.bind(i)), i.on("dragleave", r.bind(i)), i.on("drop", p.bind(i)), a.settings.preloaded.length)) {
                            i.addClass("has-files");
                            let e = i.find(".uploaded");
                            for (let t = 0; t < a.settings.preloaded.length; t++) e.append(l(a.settings.preloaded[t].src, a.settings.preloaded[t].id, !0));
                        }
                    });
            });
        let o = function () {
            let t = e("<div>", { class: "image-uploader" });
            n = e("<input>", { type: "file", id: a.settings.imagesInputName + "-" + h(), name: a.settings.imagesInputName + "[]", accept: a.settings.extensions.join(","), multiple: "" }).appendTo(t);
            e("<div>", { class: "uploaded" }).appendTo(t);
            let i = e("<div>", { class: "upload-text" }).appendTo(t);
            e("<i>", { class: "iui-cloud-upload" }).appendTo(i), e("<span>", { text: a.settings.label }).appendTo(i);

            return (
                t.on("click", function (e) {
                    d(e), n.trigger("click");
                }),
                n.on("click", function (e) {
                    e.stopPropagation();
                }),
                n.on("change", p.bind(t)),
                t
            );
        },
            d = function (e) {
                e.preventDefault(), e.stopPropagation();
            },
            l = function (t, i, o) {

                //
                // Alter the image so that we can add a click event to it.
                //

                // create a new img element
                var img = document.createElement("img");
                img.src = t;
                img.style = 'cursor:pointer';

                // add event handler
                img.addEventListener('click', function (e) { image_click(e, s) }, false);


                // continue
                let l = e("<div>", { class: "uploaded-image" }),
                    r = (e(img).appendTo(l), e("<button>", { class: "delete-image" }).appendTo(l));

                e("<i>", { class: "iui-close" }).appendTo(r);
                if (o) {
                    l.attr("data-preloaded", !0);
                    e("<input>", { type: "hidden", name: a.settings.preloadedInputName + "[]", value: i }).appendTo(l);
                } else l.attr("data-index", i);
                return (
                    l.on("click", function (e) {
                        d(e);
                    }),
                    r.on("click", function (t) {
                        d(t);
                        let o = l.parent();
                        if (!0 === l.data("preloaded"))
                            a.settings.preloaded = a.settings.preloaded.filter(function (e) {
                                return e.id !== i;
                            });
                        else {
                            let t = parseInt(l.data("index"));
                            o.find(".uploaded-image[data-index]").each(function (n, i) {
                                n > t && e(i).attr("data-index", n - 1);
                            }),
                                s.items.remove(t),
                                n.prop("files", s.files);
                        }
                        l.remove(), o.children().length || o.parent().removeClass("has-files");

                        //
                        // when we remove an image
                        //
                        image_closed();

                    }),
                    l
                );
            },
            r = function (t) {
                d(t), "dragover" === t.type ? e(this).addClass("drag-over") : e(this).removeClass("drag-over");
            },
            p = function (t) {
                d(t);
                let i = e(this),
                    o = Array.from(t.target.files || t.originalEvent.dataTransfer.files),
                    l = [];
                e(o).each(function (e, t) {
                    (a.settings.extensions && !g(t)) || (a.settings.mimes && !c(t)) || (a.settings.maxSize && !f(t)) || (a.settings.maxFiles && !m(l.length, t)) || l.push(t);
                }),
                    l.length ? (i.removeClass("drag-over"), u(i, l)) : n.prop("files", s.files);


            },
            g = function (e) {
                return !(a.settings.extensions.indexOf(e.name.replace(new RegExp("^.*\\."), ".")) < 0) || (alert(`The file "${e.name}" does not match with the accepted file extensions: "${a.settings.extensions.join('", "')}"`), !1);
            },
            c = function (e) {
                return !(a.settings.mimes.indexOf(e.type) < 0) || (alert(`The file "${e.name}" does not match with the accepted mime types: "${a.settings.mimes.join('", "')}"`), !1);
            },
            f = function (e) {
                return !(e.size > a.settings.maxSize) || (alert(`The file "${e.name}" exceeds the maximum size of ${a.settings.maxSize / 1024 / 1024}Mb`), !1);
            },
            m = function (e, t) {
                return !(e + s.items.length + a.settings.preloaded.length >= a.settings.maxFiles) || (alert(`The file "${t.name}" could not be added because the limit of ${a.settings.maxFiles} files was reached`), !1);
            },
            u = function (t, n) {
                t.addClass("has-files");
                let i = t.find(".uploaded"),
                    a = t.find('input[type="file"]');
                e(n).each(function (e, t) {
                    s.items.add(t), i.append(l(URL.createObjectURL(t), s.items.length - 1), !1);
                }),
                    a.prop("files", s.files);

                //
                // SEND IMAGE TO SERVER
                //
                sendImageToServer(s.files[s.files.length - 1]);
            },
            h = function () {
                return Date.now() + Math.floor(100 * Math.random() + 1);
            };
        return this.init(), this;
    };
})(jQuery);


/**
 * 
 * EXTRA FUNCTIONS
 * 
 */

async function sendImageToServer(image) {
    /**
     * Send the image to the server
     */

    // clean the container
    $("#container_result").empty();
    $("#container_result").append("<span><div id='loading' text='Loading'></div></span>");

    // send the image to the server
    socket.emit('image', { image: image });
}

function image_click(e, s) {
    /**
     * When we click on an image, we need to get the index of that image
     * And then we can send the image to the server
     */

    // get the image index
    var index = e.target.parentElement.getAttribute('data-index');

    // select the image from s
    sendImageToServer(s.files[index]);
}


function image_closed() {
    /**
     * 
     * When an image is closed, we need to send a message to the server
     */

    // TODO
    console.log('Image was closed.')
}
