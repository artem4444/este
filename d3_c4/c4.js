// Basic implementation of a zoomable C4 Model diagram in D3.js
// This assumes hierarchical data structured for different abstraction levels

const width = 800, height = 600;

const svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height)
    .call(d3.zoom().scaleExtent([0.5, 5]).on("zoom", zoomed))
    .append("g");

const data = {
    name: "System Context",
    children: [
        { name: "Container A", children: [
            { name: "Component A1", children: [ { name: "Code A1.1" }, { name: "Code A1.2" } ] },
            { name: "Component A2" }
        ]},
        { name: "Container B", children: [ { name: "Component B1" } ] }
    ]
};

const root = d3.hierarchy(data);
const treeLayout = d3.tree().size([width, height - 200]);
treeLayout(root);

const link = svg.selectAll(".link")
    .data(root.links())
    .enter().append("line")
    .attr("class", "link")
    .attr("x1", d => d.source.x)
    .attr("y1", d => d.source.y)
    .attr("x2", d => d.target.x)
    .attr("y2", d => d.target.y)
    .style("stroke", "#999");

const node = svg.selectAll(".node")
    .data(root.descendants())
    .enter().append("circle")
    .attr("class", "node")
    .attr("cx", d => d.x)
    .attr("cy", d => d.y)
    .attr("r", d => 10)
    .style("fill", "#69b3a2")
    .on("mouseover", (event, d) => expand(d))
    .on("mouseout", collapse);

const text = svg.selectAll(".label")
    .data(root.descendants())
    .enter().append("text")
    .attr("x", d => d.x + 12)
    .attr("y", d => d.y + 4)
    .text(d => d.data.name);

function zoomed(event) {
    svg.attr("transform", event.transform);
}

function expand(d) {
    d3.selectAll(".node").attr("r", node => node === d ? 20 : 10);
    d3.selectAll(".label").style("font-size", node => node === d ? "18px" : "12px");
}

function collapse() {
    d3.selectAll(".node").attr("r", 10);
    d3.selectAll(".label").style("font-size", "12px");
}
