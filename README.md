# Frontend for _Cleanup Catastrophe!_

work in progress!

<iframe src="not yet" id="MyFrame" style="aspect-ratio: 1/1; height: auto; width: 100%;"></iframe>
<select id="MySelectMenu">
  <option value="not yet">v.DEMO.1</option>
  <option value="not yet">v.ALPHA.1.0.0</option>
  <option value="not yet">v.ALPHA.0.5.0</option>
</select>
<button onClick="changeGame();">Change Iframe Src</button>

## DESCRIPTION
Contains (almost) all versions of _Cleanup Catastrophe!_, as single-page HTML files.

## VERSIONS
Version `v.DEMO.1` was made using Scratch 3.0, and exported using Turbowarp.

Everything else was made using Python with the pygame library, and exported using pygbag.

## NOTE
Please do not issue a pull request to this branch.

<script>
  document.getElementsByClassName('container-lg px-3 my-5 markdown-body')[0].removeChild(document.getElementsByTagName('h1')[0]);
  document.head.innerHTML += '<link rel="shortcut icon" type="image/x-icon" href="/Cleanup-Catastrophe/icon.ico">';

  function changeGame() {
    var e = document.getElementById("MySelectMenu");
    var newSrc = e.options[e.selectedIndex].value;
    document.getElementById("MyFrame").src=newSrc;
  }
</script>
