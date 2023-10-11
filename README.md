# Frontend for _Cleanup Catastrophe!_

work in progress!

<iframe src="not yet" id="MyFrame"></iframe>
<select id="MySelectMenu">
  <option value="https://beamtic.com/Examples/ip.php">Show IP</option>
  <option value="https://beamtic.com/Examples/user-agent.php">Show User Agent</option>
</select>
<button onClick="newSrc();">Change Iframe Src</button>


## DESCRIPTION
Contains (almost) all versions of _Cleanup Catastrophe!_, as single-page HTML files.

## VERSIONS
Version `v.DEMO.1` was made using Scratch 3.0, and exported using Turbowarp.

Everything else was made using Python with the pygame library, and exported using pygbag.

<script>
  document.getElementsByClassName('container-lg px-3 my-5 markdown-body')[0].removeChild(document.getElementsByTagName('h1')[0]);
  document.head.innerHTML += '<link rel="shortcut icon" type="image/x-icon" href="/Cleanup-Catastrophe/icon.ico">';

  function newSrc() {
    var e = document.getElementById("MySelectMenu");
    var newSrc = e.options[e.selectedIndex].value;
    document.getElementById("MyFrame").src=newSrc;
  }
</script>
