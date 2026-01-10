#!/usr/bin/env python3
"""
RPC Communication Layer - Lightweight VM ↔ Linux communication
Minimal overhead protocol for driver management commands

LICENSE: MIT (see LICENSE file in repository root)
"""

import socket
import json
import struct
import logging
from typing import Dict, Any, Optional, Callable
from threading import Thread, Lock

logger = logging.getLogger('RPCLayer')


class RPCProtocol:
    """
    Lightweight RPC protocol for VM-Linux communication
    Simple JSON-based protocol with minimal overhead
    """
    
    # Protocol constants
    MAGIC = b'DRVM'  # Driver VM magic bytes
    VERSION = 1
    
    # Message types
    MSG_REQUEST = 1
    MSG_RESPONSE = 2
    MSG_NOTIFICATION = 3
    
    @staticmethod
    def encode_message(msg_type: int, data: Dict[str, Any]) -> bytes:
        """
        Encode message for transmission
        
        Format: MAGIC(4) | VERSION(1) | TYPE(1) | LENGTH(4) | JSON_DATA
        
        Args:
            msg_type: Message type
            data: Message data dictionary
            
        Returns:
            Encoded bytes
        """
        json_data = json.dumps(data).encode('utf-8')
        header = struct.pack('!4sBBI', RPCProtocol.MAGIC, RPCProtocol.VERSION, msg_type, len(json_data))
        return header + json_data
    
    @staticmethod
    def decode_message(data: bytes) -> Optional[tuple[int, Dict[str, Any]]]:
        """
        Decode received message
        
        Args:
            data: Raw bytes received
            
        Returns:
            Tuple of (msg_type, data_dict) or None if invalid
        """
        try:
            # Check header
            if len(data) < 10:
                return None
            
            magic, version, msg_type, length = struct.unpack('!4sBBI', data[:10])
            
            if magic != RPCProtocol.MAGIC:
                logger.error("Invalid magic bytes")
                return None
            
            if version != RPCProtocol.VERSION:
                logger.error(f"Unsupported protocol version: {version}")
                return None
            
            # Extract JSON data
            json_data = data[10:10+length]
            data_dict = json.loads(json_data.decode('utf-8'))
            
            return (msg_type, data_dict)
        
        except Exception as e:
            logger.error(f"Failed to decode message: {e}")
            return None


class RPCClient:
    """
    RPC client for Linux-side GUI
    Connects to Windows VM and sends driver commands
    """
    
    def __init__(self, host: str = 'localhost', port: int = 9999):
        """
        Initialize RPC client
        
        Args:
            host: VM host address
            port: RPC port
        """
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
        self.lock = Lock()
    
    def connect(self, timeout: float = 5.0) -> bool:
        """
        Connect to VM RPC server
        
        Args:
            timeout: Connection timeout in seconds
            
        Returns:
            True if connected, False otherwise
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(timeout)
            self.socket.connect((self.host, self.port))
            self.connected = True
            logger.info(f"Connected to VM at {self.host}:{self.port}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to connect to VM: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """Disconnect from VM"""
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None
            self.connected = False
            logger.info("Disconnected from VM")
    
    def send_request(self, method: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Send RPC request to VM
        
        Args:
            method: Method name (e.g., 'list_drivers', 'install_driver')
            params: Method parameters
            
        Returns:
            Response data or None on error
        """
        if not self.connected:
            logger.error("Not connected to VM")
            return None
        
        with self.lock:
            try:
                # Build request
                request = {
                    'method': method,
                    'params': params
                }
                
                # Encode and send
                message = RPCProtocol.encode_message(RPCProtocol.MSG_REQUEST, request)
                self.socket.sendall(message)
                
                # Receive response
                header = self.socket.recv(10)
                if len(header) < 10:
                    logger.error("Incomplete header received")
                    return None
                
                # Parse header
                magic, version, msg_type, length = struct.unpack('!4sBBI', header)
                
                # Receive data
                data = b''
                while len(data) < length:
                    chunk = self.socket.recv(min(4096, length - len(data)))
                    if not chunk:
                        break
                    data += chunk
                
                # Decode response
                result = RPCProtocol.decode_message(header + data)
                if result:
                    msg_type, response_data = result
                    return response_data
                else:
                    return None
            
            except Exception as e:
                logger.error(f"RPC request failed: {e}")
                self.connected = False
                return None
    
    # Convenience methods for driver operations
    
    def list_drivers(self, category: Optional[str] = None) -> Optional[list]:
        """List drivers in VM"""
        response = self.send_request('list_drivers', {'category': category})
        return response.get('drivers') if response else None
    
    def install_driver(self, device_id: str) -> Optional[bool]:
        """Install driver in VM"""
        response = self.send_request('install_driver', {'device_id': device_id})
        return response.get('success') if response else None
    
    def uninstall_driver(self, device_id: str) -> Optional[bool]:
        """Uninstall driver in VM"""
        response = self.send_request('uninstall_driver', {'device_id': device_id})
        return response.get('success') if response else None
    
    def get_vm_status(self) -> Optional[Dict[str, Any]]:
        """Get VM status"""
        return self.send_request('get_status', {})


class RPCServer:
    """
    RPC server for Windows-side VM
    Receives commands from Linux GUI and executes driver operations
    """
    
    def __init__(self, host: str = '0.0.0.0', port: int = 9999):
        """
        Initialize RPC server
        
        Args:
            host: Bind address
            port: Listen port
        """
        self.host = host
        self.port = port
        self.socket = None
        self.running = False
        self.handlers = {}
    
    def register_handler(self, method: str, handler: Callable):
        """
        Register method handler
        
        Args:
            method: Method name
            handler: Handler function
        """
        self.handlers[method] = handler
        logger.info(f"Registered handler: {method}")
    
    def start(self):
        """Start RPC server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            self.running = True
            
            logger.info(f"RPC server listening on {self.host}:{self.port}")
            
            # Accept connections
            while self.running:
                try:
                    client_socket, address = self.socket.accept()
                    logger.info(f"Client connected: {address}")
                    
                    # Handle client in thread
                    thread = Thread(target=self._handle_client, args=(client_socket,))
                    thread.daemon = True
                    thread.start()
                
                except Exception as e:
                    if self.running:
                        logger.error(f"Accept error: {e}")
        
        except Exception as e:
            logger.error(f"Failed to start RPC server: {e}")
        finally:
            if self.socket:
                self.socket.close()
    
    def stop(self):
        """Stop RPC server"""
        self.running = False
        if self.socket:
            self.socket.close()
        logger.info("RPC server stopped")
    
    def _handle_client(self, client_socket: socket.socket):
        """Handle client connection"""
        try:
            while True:
                # Receive header
                header = client_socket.recv(10)
                if len(header) < 10:
                    break
                
                # Parse header
                magic, version, msg_type, length = struct.unpack('!4sBBI', header)
                
                # Receive data
                data = b''
                while len(data) < length:
                    chunk = client_socket.recv(min(4096, length - len(data)))
                    if not chunk:
                        break
                    data += chunk
                
                # Decode message
                result = RPCProtocol.decode_message(header + data)
                if not result:
                    continue
                
                msg_type, request = result
                
                # Handle request
                if msg_type == RPCProtocol.MSG_REQUEST:
                    response = self._process_request(request)
                    
                    # Send response
                    response_msg = RPCProtocol.encode_message(RPCProtocol.MSG_RESPONSE, response)
                    client_socket.sendall(response_msg)
        
        except Exception as e:
            logger.error(f"Client handler error: {e}")
        finally:
            client_socket.close()
    
    def _process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process RPC request"""
        method = request.get('method')
        params = request.get('params', {})
        
        if method not in self.handlers:
            return {
                'success': False,
                'error': f'Unknown method: {method}'
            }
        
        try:
            handler = self.handlers[method]
            result = handler(params)
            return result
        
        except Exception as e:
            logger.error(f"Handler error: {e}")
            return {
                'success': False,
                'error': str(e)
            }


def main():
    """Test RPC layer"""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='RPC Layer Test')
    parser.add_argument('mode', choices=['client', 'server'], help='Run mode')
    parser.add_argument('--port', type=int, default=9999, help='RPC port')
    
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.INFO)
    
    if args.mode == 'server':
        # Test server
        server = RPCServer(port=args.port)
        
        # Register test handler
        def test_handler(params):
            return {'success': True, 'message': 'Test response', 'params': params}
        
        server.register_handler('test', test_handler)
        
        print(f"Starting RPC server on port {args.port}...")
        print("Press Ctrl+C to stop")
        
        try:
            server.start()
        except KeyboardInterrupt:
            print("\nStopping server...")
            server.stop()
    
    else:
        # Test client
        client = RPCClient(port=args.port)
        
        print(f"Connecting to RPC server on port {args.port}...")
        if client.connect():
            print("Connected!")
            
            # Send test request
            response = client.send_request('test', {'data': 'hello'})
            print(f"Response: {response}")
            
            client.disconnect()
        else:
            print("Failed to connect")
            sys.exit(1)


if __name__ == '__main__':
    main()
