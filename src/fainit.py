from lima.models import models
from lima import faforms
import logging

log = logging.getLogger(__name__)


def includeme(config):
    config.include('pyramid_formalchemy')

    try:
        # Add fanstatic tween if available
        config.include('pyramid_fanstatic')
    except ImportError:
        log.warn('You should install pyramid_fanstatic or register a fanstatic'
                 ' middleware by hand')

    try:
        # Adding the jquery libraries if available
        config.include('fa.jquery')
    except ImportError:
        model_view = 'pyramid_formalchemy.views.ModelView'
    else:
        model_view = 'fa.jquery.pyramid.ModelView'
    """
    model_view = 'pyramid_formalchemy.views.ModelView'
    """
    session_factory = getattr(models, "DBSession", None)
    if session_factory is not None:
        # pyramid_alchemy
        session_factory = 'lima.models.models.DBSession'
    else:
        # Akhet
        session_factory = 'lima.models.models.Session'

    # register session and model_view for later use
    settings = {'package': 'lima',
                'view': model_view,
                'session_factory': session_factory,
               }
    config.registry.settings['lima.fa_config'] = settings

    config.formalchemy_admin("/admin", models=models, forms=faforms,
                             **settings)

    # Adding the package specific routes
    config.include('lima.faroutes')

    log.info('formalchemy_admin registered at /admin')
