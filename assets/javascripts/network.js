var networkGraph = {
    load: function(personId, jsonUrl) {
        sigma.parsers.json(jsonUrl, {
                renderer: {
                    container: 'network',
                    type: 'canvas'
                },
                settings: {
                    defaultNodeColor: '#607a7a',
                    defaultEdgeType: 'arrow',

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
                if (s.graph.nodes().length == 0) {
                    $('#network-container').hide();
                }

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

                sigma.plugins.tooltips(s, s.renderers[0], tooltipsConfig);

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
};

var tooltipsConfig = {
    node: [{
        show: 'hovers',
        hide: 'hovers',
        cssClass: 'sigma-tooltip',
        position: 'top',
        //autoadjust: true,
        template: '<div class="arrow"></div>' +
            ' <div class="sigma-tooltip-header">{{ label }}</div>' +
            '  <div class="sigma-tooltip-body">' +
            '    <table>' +
            '      <tr><th>Name</th> <td>{{ label }}</td></tr>' +
            '    </table>' +
            '  </div>' +
            '  <div class="sigma-tooltip-footer">Number of connections: {{ degree }}</div>',
        renderer: function(node, template) {
            // The function context is s.graph
            node.degree = this.degree(node.id);

            // Returns an HTML string:
            return Mustache.render(template, node);
        }
    }]
};
