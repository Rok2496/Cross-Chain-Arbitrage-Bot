from web3 import Web3
from typing import Dict, Any
import json
import asyncio
from eth_account import Account
import os
from dotenv import load_dotenv

class BlockchainInterface:
    def __init__(self):
        load_dotenv()
        
        # Initialize connections to different chains
        self.connections = {
            'ethereum': Web3(Web3.HTTPProvider(os.getenv('ETH_RPC_URL'))),
            'bsc': Web3(Web3.HTTPProvider(os.getenv('BSC_RPC_URL'))),
            'polygon': Web3(Web3.HTTPProvider(os.getenv('POLYGON_RPC_URL'))),
            'avalanche': Web3(Web3.HTTPProvider(os.getenv('AVAX_RPC_URL')))
        }
        
        # Bridge contracts and configurations
        self.bridge_configs = {
            'layerzero': {
                'ethereum': os.getenv('LZ_ETH_ENDPOINT'),
                'bsc': os.getenv('LZ_BSC_ENDPOINT'),
                'polygon': os.getenv('LZ_POLYGON_ENDPOINT'),
                'avalanche': os.getenv('LZ_AVAX_ENDPOINT')
            }
        }
        
        # Load contract ABIs
        self.load_contract_abis()

    def load_contract_abis(self):
        """Load all necessary contract ABIs"""
        self.abis = {
            'erc20': self.load_abi('erc20'),
            'dex': self.load_abi('dex'),
            'bridge': self.load_abi('bridge')
        }

    def load_abi(self, contract_type: str) -> dict:
        """Load ABI from file"""
        try:
            with open(f'app/contracts/{contract_type}.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: ABI file for {contract_type} not found")
            return {}

    async def execute_arbitrage(self, opportunity: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a cross-chain arbitrage opportunity"""
        result = {
            "success": False,
            "transactions": [],
            "errors": []
        }

        try:
            # 1. Execute source chain transaction
            buy_tx = await self.execute_dex_trade(
                chain=opportunity['source_chain'],
                dex=opportunity['source_dex'],
                action="buy",
                amount=opportunity['required_capital'],
                token_pair=opportunity['token_pair']
            )
            result['transactions'].append(buy_tx)

            # 2. Bridge assets if necessary
            if opportunity['source_chain'] != opportunity['target_chain']:
                bridge_tx = await self.bridge_assets(
                    from_chain=opportunity['source_chain'],
                    to_chain=opportunity['target_chain'],
                    token=opportunity['token_pair'][0],
                    amount=buy_tx['received_amount']
                )
                result['transactions'].append(bridge_tx)

            # 3. Execute target chain transaction
            sell_tx = await self.execute_dex_trade(
                chain=opportunity['target_chain'],
                dex=opportunity['target_dex'],
                action="sell",
                amount=bridge_tx['received_amount'] if 'bridge_tx' in locals() else buy_tx['received_amount'],
                token_pair=opportunity['token_pair']
            )
            result['transactions'].append(sell_tx)

            result['success'] = True

        except Exception as e:
            result['errors'].append(str(e))

        return result

    async def execute_dex_trade(self, chain: str, dex: str, action: str,
                              amount: float, token_pair: tuple) -> Dict[str, Any]:
        """Execute a trade on a DEX"""
        web3 = self.connections[chain]
        
        # This would include actual DEX interaction logic
        # Placeholder implementation
        return {
            "chain": chain,
            "dex": dex,
            "action": action,
            "amount": amount,
            "received_amount": amount * 0.99,  # Simulated slippage
            "tx_hash": "0x..."
        }

    async def bridge_assets(self, from_chain: str, to_chain: str,
                          token: str, amount: float) -> Dict[str, Any]:
        """Bridge assets between chains"""
        # This would include actual bridge interaction logic
        # Placeholder implementation
        return {
            "from_chain": from_chain,
            "to_chain": to_chain,
            "token": token,
            "amount": amount,
            "received_amount": amount * 0.995,  # Simulated bridge fee
            "tx_hash": "0x..."
        }

    async def get_balance(self, chain: str, token_address: str, wallet_address: str) -> float:
        """Get token balance for a wallet on a specific chain"""
        web3 = self.connections[chain]
        token_contract = web3.eth.contract(
            address=Web3.to_checksum_address(token_address),
            abi=self.abis['erc20']
        )
        
        balance = await token_contract.functions.balanceOf(
            Web3.to_checksum_address(wallet_address)
        ).call()
        
        return balance

    async def approve_token(self, chain: str, token_address: str,
                          spender_address: str, amount: int) -> str:
        """Approve token spending"""
        web3 = self.connections[chain]
        token_contract = web3.eth.contract(
            address=Web3.to_checksum_address(token_address),
            abi=self.abis['erc20']
        )
        
        # This would include actual approval transaction
        # Placeholder implementation
        return "0x..."  # Transaction hash 