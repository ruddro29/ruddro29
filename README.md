<svg
  width="900"
  height="400"
  viewBox="0 0 900 400"
  xmlns="http://www.w3.org/2000/svg">

  <rect
    width="900"
    height="400"
    fill="#0d1117"/>

  <style>

    .ascii {
      font-family: monospace;
      font-size: 16px;
      fill: #58a6ff;
    }

    .terminal {
      font-family: monospace;
      font-size: 22px;
      fill: #c9d1d9;
    }

    .green {
      fill: #3fb950;
    }

    .cursor {
      fill: #58a6ff;
      animation: blink 1s infinite;
    }

    @keyframes blink {
      0%, 50% {
        opacity: 1;
      }

      51%, 100% {
        opacity: 0;
      }
    }


    .typing {
  animation: typing 3s steps(6) infinite;
}

@keyframes typing {

  0% {
    clip-path: inset(0 100% 0 0);
  }

  50% {
    clip-path: inset(0 0 0 0);
  }

  100% {
    clip-path: inset(0 100% 0 0);
  }

}
    
  </style>


  <!-- ASCII NAME -->

  <text
    x="40"
    y="50"
    class="ascii">

  <tspan x="40" dy="0">
      ██████╗ ██╗   ██╗██████╗ ██████╗ ██████╗  ██████╗
    </tspan>

  <tspan x="40" dy="24">
      ██╔══██╗██║   ██║██╔══██╗██╔══██╗██╔══██╗██╔══██╗
    </tspan>

  <tspan x="40" dy="24">
      ██████╔╝██║   ██║██║  ██║██║  ██║██████╔╝██║  ██║
    </tspan>

  <tspan x="40" dy="24">
      ██╔══██╗██║   ██║██║  ██║██║  ██║██╔══██╗██║  ██║
    </tspan>

  <tspan x="40" dy="24">
      ██║  ██║╚██████╔╝██████╔╝██████╔╝██║  ██║╚█████╔╝
    </tspan>

  </text>


  <!-- TERMINAL -->

  <text
    x="40"
    y="220"
    class="terminal">

  <tspan
      x="40"
      dy="0"
      class="green">

  &gt; whoami

  </tspan>

<tspan
  x="40"
  dy="32"
  class="typing">

  Ruddro

</tspan>

  <tspan
      x="40"
      dy="32">

  &gt; building things on the internet...

  </tspan>

  </text>


  <!-- BLINKING CURSOR -->

  <rect
    x="40"
    y="292"
    width="13"
    height="24"
    class="cursor"/>

</svg>
