#!/usr/bin/env python3
"""
Real-world Integration Scenarios for PyFatFs

This demo shows practical, real-world use cases including:
- Embedded system log management
- Configuration file handling
- Data acquisition and storage
- Firmware update scenarios
- Device communication protocols
- Industrial automation data logging
"""

import sys
import os
import json
import time
import random
from datetime import datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pyfatfs import FileAccessWrapper, DirectoryAccessWrapper
import fatfs

class EmbeddedSystemLogger:
    """Simulate an embedded system that needs to log data efficiently"""
    
    def __init__(self, log_directory="system_logs"):
        self.log_directory = log_directory
        self.current_log_file = None
        self.max_log_size = 50000  # 50KB per log file
        self.log_rotation_count = 5
        
        # Create log directory
        try:
            dir_wrapper = DirectoryAccessWrapper(log_directory)
            dir_wrapper.mkdir()
            print(f"[OK] Log directory '{log_directory}' created")
        except Exception as e:
            print(f"[WARNING] Log directory may already exist: {e}")
    
    def get_current_log_filename(self):
        """Generate current log filename based on timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{self.log_directory}/system_log_{timestamp}.txt"
    
    def rotate_logs_if_needed(self):
        """Rotate logs if current file is too large"""
        if not self.current_log_file:
            return
        
        try:
            # Check current file size by reading it
            file_wrapper = FileAccessWrapper(self.current_log_file, "r")
            content = file_wrapper.read()
            file_wrapper.close()
            
            if len(content) > self.max_log_size:
                print(f"   → Rotating log file (size: {len(content)} bytes)")
                self.current_log_file = None
        except Exception as e:
            print(f"   ⚠ Error checking log size: {e}")
    
    def log_message(self, level, component, message):
        """Log a message with automatic file rotation"""
        if not self.current_log_file:
            self.current_log_file = self.get_current_log_filename()
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        log_entry = f"[{timestamp}] {level.upper():5} {component:12} | {message}\n"
        
        try:
            file_wrapper = FileAccessWrapper(self.current_log_file, "a")
            file_wrapper.write(log_entry)
            file_wrapper.close()
            
            # Check if rotation is needed
            self.rotate_logs_if_needed()
            
        except Exception as e:
            print(f"   ✗ Failed to write log entry: {e}")
    
    def simulate_system_activity(self, duration_seconds=30):
        """Simulate system activity generating logs"""
        print(f"   Simulating {duration_seconds} seconds of system activity...")
        
        components = ["SENSOR", "NETWORK", "STORAGE", "POWER", "CPU", "MEMORY"]
        levels = ["INFO", "WARN", "ERROR", "DEBUG"]
        
        start_time = time.time()
        log_count = 0
        
        while time.time() - start_time < duration_seconds:
          
            component = random.choice(components)
            level = random.choice(levels)
            
            if level == "ERROR":
                messages = [
                    "Connection timeout occurred",
                    "Memory allocation failed",
                    "Sensor reading out of range",
                    "Power supply voltage low"
                ]
            elif level == "WARN":
                messages = [
                    "High temperature detected",
                    "Network latency increased",
                    "Storage space running low",
                    "CPU usage above threshold"
                ]
            else:
                messages = [
                    "System status normal",
                    "Data packet received",
                    "Sensor calibration complete",
                    "Network connection established"
                ]
            
            message = random.choice(messages)
            self.log_message(level, component, message)
            log_count += 1
            
          
            time.sleep(random.uniform(0.1, 0.5))
        
        print(f"   ✓ Generated {log_count} log entries")

class ConfigurationManager:
    """Manage device configuration files"""
    
    def __init__(self, config_directory="device_config"):
        self.config_directory = config_directory
        self.config_file = f"{config_directory}/device_config.json"
        self.backup_file = f"{config_directory}/device_config_backup.json"
        
        
        try:
            dir_wrapper = DirectoryAccessWrapper(config_directory)
            dir_wrapper.mkdir()
            print(f"✓ Config directory '{config_directory}' created")
        except Exception as e:
            print(f"⚠ Config directory may already exist: {e}")
    
    def create_default_config(self):
        """Create a default configuration file"""
        default_config = {
            "device": {
                "id": "EMB001",
                "name": "Embedded Controller v2.1",
                "firmware_version": "1.2.3",
                "hardware_revision": "Rev C"
            },
            "network": {
                "wifi_ssid": "",
                "wifi_password": "",
                "ip_mode": "dhcp",
                "static_ip": "192.168.1.100",
                "subnet_mask": "255.255.255.0",
                "gateway": "192.168.1.1"
            },
            "sensors": {
                "temperature": {
                    "enabled": True,
                    "sample_rate": 1000,
                    "threshold_high": 85.0,
                    "threshold_low": -10.0
                },
                "pressure": {
                    "enabled": True,
                    "sample_rate": 500,
                    "threshold_high": 1013.25,
                    "threshold_low": 950.0
                }
            },
            "system": {
                "log_level": "INFO",
                "watchdog_timeout": 30,
                "auto_restart": True,
                "data_retention_days": 30
            }
        }
        
        try:
            config_json = json.dumps(default_config, indent=2)
            file_wrapper = FileAccessWrapper(self.config_file, "w")
            file_wrapper.write(config_json)
            file_wrapper.close()
            print("   ✓ Default configuration created")
            return True
        except Exception as e:
            print(f"   ✗ Failed to create default config: {e}")
            return False
    
    def load_config(self):
        """Load configuration from file"""
        try:
            file_wrapper = FileAccessWrapper(self.config_file, "r")
            config_json = file_wrapper.read()
            file_wrapper.close()
            
            config = json.loads(config_json)
            print("   ✓ Configuration loaded successfully")
            return config
        except Exception as e:
            print(f"   ✗ Failed to load config: {e}")
            return None
    
    def save_config(self, config):
        """Save configuration to file with backup"""
        try:
            # Create backup of current config
            try:
                file_wrapper = FileAccessWrapper(self.config_file, "r")
                current_config = file_wrapper.read()
                file_wrapper.close()
                
                backup_wrapper = FileAccessWrapper(self.backup_file, "w")
                backup_wrapper.write(current_config)
                backup_wrapper.close()
                print("   ✓ Configuration backup created")
            except:
                print("   ⚠ Could not create backup (file may not exist)")
            
            # Save new configuration
            config_json = json.dumps(config, indent=2)
            file_wrapper = FileAccessWrapper(self.config_file, "w")
            file_wrapper.write(config_json)
            file_wrapper.close()
            print("   ✓ Configuration saved")
            return True
            
        except Exception as e:
            print(f"   ✗ Failed to save config: {e}")
            return False
    
    def update_config_value(self, section, key, value):
        """Update a specific configuration value"""
        config = self.load_config()
        if not config:
            return False
        
        if section in config and key in config[section]:
            old_value = config[section][key]
            config[section][key] = value
            
            if self.save_config(config):
                print(f"   ✓ Updated {section}.{key}: {old_value} → {value}")
                return True
        
        print(f"   ✗ Configuration key {section}.{key} not found")
        return False

class DataAcquisitionSystem:
    """Simulate a data acquisition system storing sensor readings"""
    
    def __init__(self, data_directory="sensor_data"):
        self.data_directory = data_directory
        
        # Create data directory structure
        try:
            dir_wrapper = DirectoryAccessWrapper(data_directory)
            dir_wrapper.mkdir()
            
            for subdir in ["temperature", "pressure", "humidity", "voltage"]:
                sub_wrapper = DirectoryAccessWrapper(f"{data_directory}/{subdir}")
                sub_wrapper.mkdir()
            
            print(f"✓ Data acquisition directory structure created")
        except Exception as e:
            print(f"⚠ Data directories may already exist: {e}")
    
    def generate_sensor_data(self, sensor_type, num_samples=100):
        """Generate realistic sensor data"""
        data = []
        base_time = time.time()
        
        # Different sensor characteristics
        if sensor_type == "temperature":
            base_value = 22.0
            noise_range = 0.5
            trend = 0.01
        elif sensor_type == "pressure":
            base_value = 1013.25
            noise_range = 2.0
            trend = -0.05
        elif sensor_type == "humidity":
            base_value = 45.0
            noise_range = 1.0
            trend = 0.02
        elif sensor_type == "voltage":
            base_value = 5.0
            noise_range = 0.1
            trend = 0.0
        else:
            base_value = 0.0
            noise_range = 1.0
            trend = 0.0
        
        for i in range(num_samples):
            timestamp = base_time + i * 1.0  # 1 second intervals
            noise = random.uniform(-noise_range, noise_range)
            trend_value = trend * i
            value = base_value + noise + trend_value
            
            data.append({
                "timestamp": timestamp,
                "value": round(value, 3),
                "quality": random.choice(["good", "good", "good", "fair", "poor"])  # Mostly good
            })
        
        return data
    
    def save_sensor_data(self, sensor_type, data):
        """Save sensor data to CSV-like format"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.data_directory}/{sensor_type}/data_{timestamp}.csv"
        
        try:
            file_wrapper = FileAccessWrapper(filename, "w")
            
            # Write header
            file_wrapper.write("timestamp,value,quality\n")
            
            # Write data
            for sample in data:
                line = f"{sample['timestamp']},{sample['value']},{sample['quality']}\n"
                file_wrapper.write(line)
            
            file_wrapper.close()
            print(f"   ✓ Saved {len(data)} {sensor_type} samples to {filename}")
            return True
            
        except Exception as e:
            print(f"   ✗ Failed to save {sensor_type} data: {e}")
            return False
    
    def simulate_data_collection(self, duration_minutes=2):
        """Simulate continuous data collection"""
        print(f"   Simulating {duration_minutes} minutes of data collection...")
        
        sensors = ["temperature", "pressure", "humidity", "voltage"]
        start_time = time.time()
        collection_count = 0
        
        while time.time() - start_time < duration_minutes * 60:
            for sensor in sensors:
                # Collect a batch of samples
                data = self.generate_sensor_data(sensor, 10)
                self.save_sensor_data(sensor, data)
                collection_count += 1
            
            # Wait before next collection cycle
            time.sleep(10)  # 10 second intervals
        
        print(f"   ✓ Completed {collection_count} data collection cycles")

class FirmwareUpdateManager:
    """Manage firmware update process with file integrity"""
    
    def __init__(self, firmware_directory="firmware"):
        self.firmware_directory = firmware_directory
        
        try:
            dir_wrapper = DirectoryAccessWrapper(firmware_directory)
            dir_wrapper.mkdir()
            print(f"✓ Firmware directory created")
        except Exception as e:
            print(f"⚠ Firmware directory may already exist: {e}")
    
    def create_mock_firmware(self, version, size_kb=256):
        """Create a mock firmware file for testing"""
        filename = f"{self.firmware_directory}/firmware_v{version}.bin"
        
        # Generate mock firmware data (repeating pattern)
        pattern = f"FIRMWARE_V{version}_DATA"
        firmware_data = (pattern * (size_kb * 1024 // len(pattern) + 1))[:size_kb * 1024]
        
        try:
            file_wrapper = FileAccessWrapper(filename, "w")
            file_wrapper.write(firmware_data)
            file_wrapper.close()
            print(f"   ✓ Created mock firmware: {filename} ({size_kb}KB)")
            return filename
        except Exception as e:
            print(f"   ✗ Failed to create firmware: {e}")
            return None
    
    def verify_firmware_integrity(self, filename):
        """Simple firmware integrity check"""
        try:
            file_wrapper = FileAccessWrapper(filename, "r")
            content = file_wrapper.read()
            file_wrapper.close()
            
            # Simple checksum (count characters)
            checksum = sum(ord(c) for c in content) % 65536
            
            print(f"   ✓ Firmware integrity check: {len(content)} bytes, checksum: {checksum}")
            return True
            
        except Exception as e:
            print(f"   ✗ Firmware integrity check failed: {e}")
            return False
    
    def simulate_firmware_update(self):
        """Simulate a complete firmware update process"""
        print("   Simulating firmware update process...")
        
        # Step 1: Create current firmware
        current_firmware = self.create_mock_firmware("1.2.3", 256)
        if not current_firmware:
            return False
        
        # Step 2: Verify current firmware
        if not self.verify_firmware_integrity(current_firmware):
            return False
        
        # Step 3: Create new firmware
        new_firmware = self.create_mock_firmware("1.3.0", 268)
        if not new_firmware:
            return False
        
        # Step 4: Verify new firmware
        if not self.verify_firmware_integrity(new_firmware):
            return False
        
        # Step 5: Backup current firmware
        backup_file = f"{self.firmware_directory}/firmware_backup.bin"
        try:
            # Read current firmware
            file_wrapper = FileAccessWrapper(current_firmware, "r")
            backup_data = file_wrapper.read()
            file_wrapper.close()
            
            # Write backup
            backup_wrapper = FileAccessWrapper(backup_file, "w")
            backup_wrapper.write(backup_data)
            backup_wrapper.close()
            print("   ✓ Firmware backup created")
            
        except Exception as e:
            print(f"   ✗ Firmware backup failed: {e}")
            return False
        
        print("   ✓ Firmware update simulation completed")
        return True

def demonstrate_embedded_logging():
    """Demo embedded system logging"""
    print("=== Embedded System Logging Demo ===")
    
    logger = EmbeddedSystemLogger()
    
    # Manual log entries
    logger.log_message("INFO", "SYSTEM", "System initialization started")
    logger.log_message("INFO", "NETWORK", "WiFi connection established")
    logger.log_message("WARN", "SENSOR", "Temperature sensor calibration needed")
    logger.log_message("ERROR", "STORAGE", "SD card write error detected")
    logger.log_message("INFO", "SYSTEM", "System initialization completed")
    
    # Simulate continuous logging
    logger.simulate_system_activity(5)  # 5 seconds of activity

def demonstrate_configuration_management():
    """Demo configuration file management"""
    print("\n=== Configuration Management Demo ===")
    
    config_mgr = ConfigurationManager()
    
    # Create and load default configuration
    config_mgr.create_default_config()
    config = config_mgr.load_config()
    
    if config:
        print("   Current device configuration:")
        print(f"     Device ID: {config['device']['id']}")
        print(f"     Firmware: {config['device']['firmware_version']}")
        print(f"     WiFi SSID: {config['network']['wifi_ssid'] or '(not configured)'}")
        print(f"     Log Level: {config['system']['log_level']}")
    
    # Update some configuration values
    config_mgr.update_config_value("network", "wifi_ssid", "ProductionNetwork")
    config_mgr.update_config_value("system", "log_level", "DEBUG")
    config_mgr.update_config_value("sensors", "temperature", {"enabled": True, "sample_rate": 2000})

def demonstrate_data_acquisition():
    """Demo data acquisition and storage"""
    print("\n=== Data Acquisition System Demo ===")
    
    daq_system = DataAcquisitionSystem()
    
    # Generate and save sample data for each sensor type
    sensors = ["temperature", "pressure", "humidity", "voltage"]
    for sensor in sensors:
        print(f"   Collecting {sensor} data...")
        data = daq_system.generate_sensor_data(sensor, 50)
        daq_system.save_sensor_data(sensor, data)
    
    # Simulate brief data collection period
    daq_system.simulate_data_collection(0.5)  # 30 seconds

def demonstrate_firmware_management():
    """Demo firmware update management"""
    print("\n=== Firmware Update Management Demo ===")
    
    fw_manager = FirmwareUpdateManager()
    fw_manager.simulate_firmware_update()

def main():
    """Run comprehensive real-world integration demo"""
    print("PyFatFs Real-world Integration Scenarios Demo")
    print("=" * 55)
    
    try:
        # Initialize file system
        print("Initializing file system...")
        result = fatfs.mount("", 0, 1)
        if result == 0:
            print("✓ File system mounted successfully")
        else:
            print(f"⚠ Mount returned code: {result} (continuing with demo)")
        
        # Run real-world scenarios
        demonstrate_embedded_logging()
        demonstrate_configuration_management()
        demonstrate_data_acquisition()
        demonstrate_firmware_management()
        
        print("\n" + "=" * 55)
        print("Real-world integration demo completed!")
        print("\nThis demo showed practical applications including:")
        print("• Embedded system logging with automatic rotation")
        print("• Configuration file management with backup")
        print("• Data acquisition and sensor data storage")
        print("• Firmware update process with integrity checking")
        print("\nThese patterns can be adapted for your specific use case.")
        
    except Exception as e:
        print(f"Demo failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()