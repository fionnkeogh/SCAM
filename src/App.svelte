<script>
  //@ts-nocheck
  import Init from './lib/Init/Init.svelte';
  import Simulator from './lib/Simulator/Simulator.svelte';

  const pages = [Init, Simulator];
  let page = 0;

  function openPage(_page) {
    page = _page;
    return page;
  }

  function pythonToJS(object) {
    if(object.toString() == "None") {
      return undefined;
    }
    return JSON.parse(object.toString().replaceAll(/'/g, '"'))
  }
</script>

<svelte:component
  this={pages[page]} 
  openPage={openPage}
  pythonToJS={pythonToJS} />
