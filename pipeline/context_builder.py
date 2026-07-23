class ContextBuilder:

    def build(self, subgraph):

        lines = []

        # Entities
        lines.append("## Entity Information\n")

        for entity in subgraph.entities.values():
            lines.append(f"Entity: {entity.name}")

            if entity.entity_type:
                lines.append(f"Type: {entity.entity_type}")

            if entity.description:
                lines.append(
                    f"Description: {entity.description}"
                )

            lines.append("")

        # Relations
        lines.append("## Relationship Information\n")

        for relation in subgraph.relations:
            source = subgraph.entities[relation.source].name
            target = subgraph.entities[relation.target].name

            lines.append(
                f"- {source} {relation.relation} {target}"
            )

        return "\n".join(lines)