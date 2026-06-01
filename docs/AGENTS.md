# ScrapingBusiness â€” AI Agent Instructions

## Memory (agentmemory)
agentmemory estÃ¡ corriendo en localhost:3111 y tienes herramientas MCP disponibles.

- **AL INICIAR**: ejecuta memory_context para cargar el contexto del proyecto
- **AL FINALIZAR**: ejecuta memory_save con el tipo "session" para guardar un resumen de lo hecho
- **AL APRENDER ALGO IMPORTANTE**: ejecuta memory_save con tipo "decision" o "pattern"
- **ANTES DE CAMBIAR CÃ“DIGO**: ejecuta memory_smart_search con lo que quieres hacer para ver si hay contexto relevante
- Usa project: "ScrapingBusiness" en todas las operaciones
