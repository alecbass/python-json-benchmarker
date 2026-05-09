import { useEffect, useState } from "react";
import { Code, Deck, Fragment, Slide } from "@revealjs/react";
import Reveal from "reveal.js";
import Markdown from "reveal.js/plugin/markdown";
import RevealHighlight from "reveal.js/plugin/highlight";

import "./App.css";

function App() {
  const [count, setCount] = useState(0);

  return (
    <Deck plugins={[Markdown, RevealHighlight]}>
      <Slide>
        <h1>My Cool Talk</h1>
        <p>:)</p>
        <Fragment as="p">First point</Fragment>
        <Fragment as="p">Second point</Fragment>
        <Fragment asChild>
          <p>Third point</p>
        </Fragment>
      </Slide>

      <Slide background="#111827">
        <h2>Second slide</h2>
        <Code language="javascript">
          {`const greeting = 'Hello, world!';
console.log(greeting);`}
        </Code>
      </Slide>

      <Slide>
        <p>Chapter One</p>
        <h1>The Beginning</h1>
        {/* TODO(alec): Come up with a story */}
      </Slide>

      <Slide>
        <h1>Me</h1>
        <p>Me!</p>
        <ul>
          <Fragment as="li">Python + TypeScript + Rust (sometimes)</Fragment>
          <Fragment as="li">Mostly in web development</Fragment>
        </ul>
      </Slide>

      <Slide>
        <p>Interests</p>
        <ul>
          <Fragment as="li">Developer experience</Fragment>
          <Fragment as="li">Optimisation</Fragment>
        </ul>
      </Slide>

      <Slide>
        <p>What this talk is</p>
        <ul>
          <Fragment as="li">
            How Python performance can be increased through native code
          </Fragment>
          <Fragment as="li">
            Whether you should use native code in your Python library
          </Fragment>
          <Fragment as="li">Drawbacks to each approach</Fragment>
        </ul>
      </Slide>

      <Slide>
        <p>
          What this talk is <b>NOT</b>
        </p>
        <ul>
          <Fragment as="li">How to write good Rust</Fragment>
          <Fragment as="li">
            Giving a concrete yes/no as to whether you should use it
          </Fragment>
        </ul>
      </Slide>

      <Slide>
        <h1>Language Comparisons</h1>
        <p>What is native code?</p>
        <ul>
          <Fragment as="li">Code which runs directly as machine code</Fragment>
          <Fragment as="li">
            Often written in languages such as C, C++, Rust, Go etc.
          </Fragment>
          <Fragment as="li">
            Platform-specific - dependent on processor architecture, operating
            system
          </Fragment>
        </ul>
      </Slide>

      <Slide>
        <h1>Different type of programming languages</h1>
      </Slide>

      <Slide>
        <h1>The core: Assembly (machine code)</h1>
        <Code language="assembly">{`mv r16, r17`}</Code>
      </Slide>

      <Slide>
        <h1>Ahead of time compilation: Assembly</h1>
        {/* TODO(alec): Show photos of C, C++, Rust, Go, Zig */}
      </Slide>

      <Slide>
        <h1>Ahead of time compilation: Bytecode</h1>
        {/* TODO(alec): Show photos of Java and C# */}
      </Slide>

      <Slide>
        <h1>Just in time compilation</h1>
        {/* TODO(alec): Show photos of Python and JavaScript */}
      </Slide>

      <Slide>
        <h1>Software with performance constraints</h1>
        <ul>
          <li>Industrial mathematics</li>
          <li>Embedded software</li>
          <li>Databases</li>
          <li>Operating systems</li>
        </ul>
      </Slide>

      <Slide>
        <h1>Commercial Python</h1>
        <ul>
          <li>Lots of stuff, honestly</li>
          <li>Scripting</li>
          <li>Web development</li>
          <li>Scientific Research</li>
          <li>Artificial Intelligence</li>
        </ul>
      </Slide>
    </Deck>
  );
}

export default App;
