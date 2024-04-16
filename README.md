# Frontend for _Cleanup Catastrophe!_

<select id="selectVer">
  <option value="https://html-classic.itch.zone/html/9822033/index.html">demo 1.0</option>
  <option value="https://rawcdn.githack.com/richkdev/Cleanup-Catastrophe/4abe9cb7fbad4f0503230a72d68792ff03024907/build/web/index.html">v.0.1.1-alpha</option>
  <option value="https://rawcdn.githack.com/richkdev/Cleanup-Catastrophe/34573e94c2472da324d80eda95a47cd9f58d6914/build/web/index.html">v.0.1.0-alpha</option>
</select>
<button onClick="changeGame();">Change versions</button>
<iframe src="data:text/plain;charset=utf-8,Choose%20a%20version%20to%20start%20playing!" id="game" style="height: 25em; width: 100%;">Your browser does not support iframes.</iframe>

<script>
  document.getElementsByClassName('container-lg px-3 my-5 markdown-body')[0].removeChild(document.getElementsByTagName('h1')[0]);
  document.head.innerHTML += '<link rel="shortcut icon" type="image/x-icon" href="/Cleanup-Catastrophe/icon.ico">';

  function changeGame() {
    var e = document.getElementById("selectVer");
    document.getElementById("game").src = e.options[e.selectedIndex].value;
  }
</script>
