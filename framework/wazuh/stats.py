# Copyright (C) 2015-2021, Wazuh Inc.
# Created by Wazuh, Inc. <info@wazuh.com>.
# This program is free software; you can redistribute it and/or modify it under the terms of GPLv2


from wazuh.core.agent import Agent, get_agents_info
from wazuh.core.cluster.cluster import get_node
from wazuh.core.cluster.utils import read_cluster_config
from wazuh.core.results import AffectedItemsWazuhResult
from wazuh.core.stats import get_daemons_stats_, hourly_, totals_, weekly_
from wazuh.core.exception import WazuhInternalError, WazuhException, WazuhResourceNotFound
from wazuh.rbac.decorators import expose_resources

cluster_enabled = not read_cluster_config(from_import=True)['disabled']
node_id = get_node().get('node') if cluster_enabled else None


@expose_resources(actions=[f"{'cluster' if cluster_enabled else 'manager'}:read"],
                  resources=[f'node:id:{node_id}' if cluster_enabled else '*:*:*'])
def totals(date):
    """Retrieve statistical information for the current or specified date.

    Parameters
    ----------
    date: date
        Date object with the date value of the stats.

    Returns
    -------
    AffectedItemsWazuhResult
        Array of dictionaries. Each dictionary represents an hour.
    """
    result = AffectedItemsWazuhResult(all_msg='Statistical information for each node was successfully read',
                                      some_msg='Could not read statistical information for some nodes',
                                      none_msg='Could not read statistical information for any node'
                                      )
    failed, affected = totals_(date)
    if failed:
        result.add_failed_item(id_=node_id if cluster_enabled else 'manager', error=WazuhInternalError(1309))
    result.affected_items = affected
    result.total_affected_items = len(result.affected_items)

    return result


@expose_resources(actions=[f"{'cluster' if cluster_enabled else 'manager'}:read"],
                  resources=[f'node:id:{node_id}' if cluster_enabled else '*:*:*'])
def hourly():
    """Compute hourly averages.

    Returns
    -------
    AffectedItemsWazuhResult
        Dictionary with averages and interactions.
    """
    result = AffectedItemsWazuhResult(all_msg='Statistical information per hour for each node was successfully read',
                                      some_msg='Could not read statistical information per hour for some nodes',
                                      none_msg='Could not read statistical information per hour for any node'
                                      )
    result.affected_items = hourly_()
    result.total_affected_items = len(result.affected_items)

    return result


@expose_resources(actions=[f"{'cluster' if cluster_enabled else 'manager'}:read"],
                  resources=[f'node:id:{node_id}' if cluster_enabled else '*:*:*'])
def weekly():
    """Compute weekly averages.

    Returns
    -------
    AffectedItemsWazuhResult
        Dictionary for each week day.
    """
    result = AffectedItemsWazuhResult(all_msg='Statistical information per week for each node was successfully read',
                                      some_msg='Could not read statistical information per week for some nodes',
                                      none_msg='Could not read statistical information per week for any node'
                                      )
    result.affected_items = weekly_()
    result.total_affected_items = len(result.affected_items)

    return result


@expose_resources(actions=[f"{'cluster' if cluster_enabled else 'manager'}:read"],
                  resources=[f'node:id:{node_id}' if cluster_enabled else '*:*:*'])
def get_daemons_stats(filename):
    """Get daemons stats from an input file.

    Parameters
    ----------
    filename: str
        Full path of the file to get information.

    Returns
    -------
    AffectedItemsWazuhResult
        Dictionary with the stats of the input file.
    """
    result = AffectedItemsWazuhResult(
        all_msg='Statistical information for each node was successfully read',
        some_msg='Could not read statistical information for some nodes',
        none_msg='Could not read statistical information for any node'
        )
    result.affected_items = get_daemons_stats_(filename)
    result.total_affected_items = len(result.affected_items)

    return result


@expose_resources(actions=["agent:read"], resources=["agent:id:{agent_list}"], post_proc_func=None)
def get_agents_component_stats_json(agent_list=None, component=None):
    """Get statistics of an agent's component.

    Parameters
    ----------
    agent_list: list, optional
        List of agents ID's, by default None.
    component: str, optional
        Name of the component to get stats from, by default None.

    Returns
    -------
    AffectedItemsWazuhResult
        Component stats.
    """
    result = AffectedItemsWazuhResult(all_msg='Statistical information for each agent was successfully read',
                                      some_msg='Could not read statistical information for some agents',
                                      none_msg='Could not read statistical information for any agent')
    system_agents = get_agents_info()
    for agent_id in agent_list:
        try:
            if agent_id not in system_agents:
                raise WazuhResourceNotFound(1701)
            result.affected_items.append(Agent(agent_id).get_stats(component=component))
        except WazuhException as e:
            result.add_failed_item(id_=agent_id, error=e)
    result.total_affected_items = len(result.affected_items)

    return result
