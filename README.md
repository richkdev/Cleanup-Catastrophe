# Frontend for _Cleanup Catastrophe!_

<select id="selectVer">
  <option value="#">demo #1</option>
  <option value="https://rawcdn.githack.com/richkdev/Cleanup-Catastrophe/4abe9cb7fbad4f0503230a72d68792ff03024907/build/web/index.html">v.0.1.1-alpha</option>
  <option value="https://rawcdn.githack.com/richkdev/Cleanup-Catastrophe/34573e94c2472da324d80eda95a47cd9f58d6914/build/web/index.html">v.0.1.0-alpha</option>
</select>
<button onClick="changeGame();">Change versions</button>
<iframe src="not yet" id="game" style="height: 25em; width: 100%;">Your browser does not support iframes.</iframe>

<script>
  document.getElementsByClassName('container-lg px-3 my-5 markdown-body')[0].removeChild(document.getElementsByTagName('h1')[0]);
  document.head.innerHTML += '<link rel="shortcut icon" type="image/x-icon" href="/Cleanup-Catastrophe/icon.ico">';

  function changeGame() {
    var e = document.getElementById("selectVer");
    document.getElementById("game").src = e.options[e.selectedIndex].value;
  }
</script>
