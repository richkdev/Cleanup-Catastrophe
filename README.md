# Frontend for _Cleanup Catastrophe!_ (work in progress)
<select id="selectVer">
  <option value="?">v.DEMO.1.0.0</option>
  <option value="?">v.ALPHA.1.0.0</option>
  <option value="?">v.ALPHA.0.5.0</option>
</select>
<button onClick="changeGame();">Change versions</button>
<iframe src="not yet" id="game" style="aspect-ratio: 1/1; height: auto; width: 25em;"></iframe>

## DESCRIPTION
Contains (almost) all versions of _Cleanup Catastrophe!_, as single-page HTML files.

## VERSIONS
Version `v.DEMO.1.0.0` was made using Scratch 3.0, and exported using Turbowarp.

Everything else was made using Python with the pygame library, and exported using pygbag.

## NOTE
Please do not issue a pull request to this branch.

<script src="https://cdn.jsdelivr.net/npm/darkmode-js@1.5.7/lib/darkmode-js.min.js"></script>
<script>
  document.getElementsByClassName('container-lg px-3 my-5 markdown-body')[0].removeChild(document.getElementsByTagName('h1')[0]);
  document.head.innerHTML += '<link rel="shortcut icon" type="image/x-icon" href="/Cleanup-Catastrophe/icon.ico">';

  function changeGame() {
    var e = document.getElementById("selectVer");
    document.getElementById("game").src = e.options[e.selectedIndex].value;
  }
  
  function addDarkmodeWidget() {
    new Darkmode().showWidget();
  }
  window.addEventListener('load', addDarkmodeWidget);

  ddocument.getElementsByClassName('darkmode-toggle')[0].textContent = '🌓';
</script>
