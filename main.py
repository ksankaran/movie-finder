import click
import httpx

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore, InMemoryPushNotifier
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from agent import MovieFinderAgent
from agent_executor import MovieFinderAgentExecutor

def app(host: str = None, port: int = None) -> A2AStarletteApplication:
    """Creates and returns the A2AStarletteApplication instance."""
    url = f"http://{host}:{port}"
    capabilities = AgentCapabilities(streaming=True, pushNotifications=False)
    skill = AgentSkill(
        id='movie_finder_agent',
        name='Find Movies using scene descriptions',
        description='Search movies using vector embeddings based on scene descriptions.',
        tags=['movie', 'search', 'vector', 'embeddings'],
        examples=[
            'Find movies with a hero named Matrix who worked in the army.',
            'Search for movies where the hero is a soldier named Matrix.',
            'blue tiny creature with a red hat and a yellow shirt',
        ],
    )
    agent_card = AgentCard(
        name='Movie Finder Agent',
        description='An agent that helps find movies based on scene descriptions using vector embeddings.',
        url=url,
        version='1.0.0',
        defaultInputModes=MovieFinderAgent.SUPPORTED_CONTENT_TYPES,
        defaultOutputModes=MovieFinderAgent.SUPPORTED_CONTENT_TYPES,
        capabilities=capabilities,
        skills=[skill],
    )

    httpx_client = httpx.AsyncClient()
    task_store = InMemoryTaskStore()
    request_handler = DefaultRequestHandler(
        agent_executor=MovieFinderAgentExecutor(),
        task_store=task_store,
        push_notifier=InMemoryPushNotifier(httpx_client),
    )
    server = A2AStarletteApplication(
        agent_card=agent_card, http_handler=request_handler
    )

    return server.build()

@click.command()
@click.option('--host', 'host', default='localhost')
@click.option('--port', 'port', default=8080)
def main(host, port):
    """Starts the Movie Finder Agent server."""
    try:
        agent_app = app(host, port)

        import uvicorn

        uvicorn.run(agent_app, host=host, port=port)

    except Exception as e:
        print(f'An error occurred during server startup: {e}')
        exit(1)


if __name__ == '__main__':
    main()