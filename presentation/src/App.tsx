import { useEffect, useState } from "react";
import { Code, Deck, Fragment, Slide } from "@revealjs/react";
import Reveal from "reveal.js";
import Markdown from "reveal.js/plugin/markdown";

import "./App.css";

function App() {
  const [count, setCount] = useState(0);

  return (
    <Deck plugins={[Markdown]}>
      <Slide>
        <h1>Hello</h1>
        <p>My first Reveal deck in React.</p>
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
    </Deck>
  );
}

export default App;
