#from distutils.command.config import config
from scripts.helpful_scripts import fund_with_link, get_account, OPENSEA_URL, get_contract
from brownie import AdvancedCollectible, network, config
#from web3 import Web3

def main():
    deploy_and_create()


def deploy_and_create():
    account = get_account()
    advanced_collectible = AdvancedCollectible.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account})

    fund_with_link(advanced_collectible.address)
    creating_tx = advanced_collectible.createCollectible({"from": account})
    creating_tx.wait(1)
    print("New Token!")
    return advanced_collectible, creating_tx