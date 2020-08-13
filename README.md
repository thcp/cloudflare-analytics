# Cloudflare Analytics parser and dashboard 

![](http://i.imgur.com/DnGdaj2.png)

  

Multi-container Docker app built from the following services:

  

*  [InfluxDB](https://github.com/influxdata/influxdb) - time series database

*  [Grafana](https://github.com/grafana/grafana) - visualization UI for InfluxDB

  
  

## General information

#### Volumes

For development purposes, volumes are purposely commented. If you wish to enable persistence, enable uncomment the required volumes. on `docker-compose.yml` file

  

### Users

  

Two admin users are provisioned, one for InfluxDB and one for Grafana. By default, the username of both accounts is `admin` and password is defined to `localtestsonly` to enforce the purpose of a test environment. To override the default credentials, set the following environment variables on `.env` file before starting the app

  

### Database

  

Default InfluxDB database called `cloudflare`.

  

### Data Sources

  

By default, datasource `InfluxDB` will be provisioned to connected to the default IndfluxDB database. if you wish to change any value you must edit `grafana/datasource/datasources.yaml` file

  

### Dashboards
Default dashboard is installed during the startup process, file location can be found under `grafana/datasource/`. 

**Important note:** Before using the dashboard, go to `dashboard settings/variables` and click on update to refresh the domain list.

  

### Plugins

Currently `grafana-worldmap-panel` will be installed as dependency of the dashboard. If you with to install more plugins update `.env` file variable `GRAFANA_PLUGINS` with the desired plugins separated by comma.

  

## Deployment options

  

### Development mode

  

1. Install [docker-compose](https://docs.docker.com/compose/install/) on the docker host.

1. Clone this repo on the docker host.

1. Optionally, change default credentials or Grafana provisioning.

1. Run the following command from the root of the cloned repo:

```

docker-compose up -d

```

  

To stop the app:

  

1. Run the following command from the root of the cloned repo:

```

docker-compose down

```

### Production mode

Still in progress.
  

#### Ports

  

Exported ports:

| Host Port | Service |
|--|--|
| 3000 | Grafana |
| 8086 | InfluxDB |
