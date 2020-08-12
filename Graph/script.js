
//<![CDATA[

var svgFile = document.getElementById("svgFile");
//var divFile = document.getElementById("divFile");

svgFile.addEventListener("load",function() {
      var svgContant = svgFile.contentDocument;

      var acc = svgContant.getElementsByClassName("edge");

      var size = acc.length;

      var i = 0;

      for (; i < size; i++) {

          for (var k = 0; k < acc[i].childNodes.length; k++) {

              if (acc[i].childNodes[k].tagName === "g") {
                  acc[i].childNodes[k].style.display = "none";

              }
          }

          acc[i].addEventListener("click", function(event) {

              elems = event.target.parentNode.childNodes;

                for (var j = 0; j < elems.length; j++){

                  if (elems[j].tagName === "g"){
                      if (elems[j].style.display === "none"){
                          elems[j].style.display = "table";
                    }
                    else{
                        elems[j].style.display = "none";
                    }
                  }
                }
                },false);
      }

      var icons = svgContant.getElementsByClassName("icon");
      var size_icons = icons.length;

      var f = 0;
      for (; f < size_icons; f++) {

          icons[f].addEventListener("mouseover", showPopup);

          icons[f].addEventListener("mouseout", hidePopup);
      }
      }, false);

    function showPopup(evt) {
        var elem = evt.target.parentElement;

        var iconPos = elem.getBoundingClientRect();
        var id = "info_".concat(elem.id.substring(5));
        var paragraph = document.getElementById(id);

        paragraph.style.left = (iconPos.right + 20) + "px";
        paragraph.style.top = (iconPos.top - 57) + "px";

        paragraph.style.display = "block";
    }

    function hidePopup(evt) {
        var elem = evt.target.parentElement;
        var id = "info_".concat(elem.id.substring(5));

        var paragraph = document.getElementById(id);

        paragraph.style.display = "none";

    }
//]]>
