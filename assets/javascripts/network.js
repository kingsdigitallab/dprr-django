var networkGraph = {
    load: function(personId, jsonUrl) {
        sigma.parsers.json(jsonUrl, {
                renderer: {
                    container: 'network',
                    type: 'canvas'
                },
                settings: {
                    defaultNodeColor: '#607a7a',

                    minNodeSize: 1,
                    maxNodeSize: 10,
                    minEdgeSize: 1,
                    maxEdgeSize: 2,

                    enableEdgeHovering: true,
                    edgeHoverColor: 'edge',
                    defaultEdgeHoverColor: '#000',
                    edgeHoverSizeRatio: 2,
                    edgeHoverExtremities: true,

                    autoCurveRatio: 2
                }
            },
            function(s) {
                // puts nodes in a circle
                s.graph.nodes().forEach(function(node, i, nodes) {
                    node.size = 3;

                    if (node.id == personId) {
                        node.color = '#363635';
                        node.x = 0;
                        node.y = 0;
                    } else {
                        node.x = -Math.cos(Math.PI * 2 * i / nodes.length);
                        node.y = Math.sin(Math.PI * 2 * i / nodes.length);
                    }
                });

                s.graph.edges().forEach(function(edge, i, edges) {
                    edge.size = 2;
                });

                sigma.canvas.edges.autoCurve(s);

                sigma.plugins.dragNodes(s, s.renderers[0]);

                s.refresh();

                // configure the ForceLink algorithm
                fa = sigma.layouts.configForceLink(s, {
                    worker: true,
                    autoStop: true,
                    background: true,
                    easing: 'cubicInOut'
                });

                // start the ForceLink algorithm
                sigma.layouts.startForceLink();
            });
    }
}
