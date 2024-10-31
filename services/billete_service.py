import torch
from torchvision import transforms
from PIL import Image
from models.billete_classifier import BilleteClassifier  # Importar la clase

class BilleteService:
    def __init__(self, model_path='modelo_billetesMixto.pth'): 

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
        self.model = BilleteClassifier(num_classes=42)
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.eval()  
        self.model.to(self.device)
        
        self.transform = transforms.Compose([
            transforms.Resize((416, 416)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    
    def predict(self, image_file):
        image = Image.open(image_file).convert('RGB')
        image = self.transform(image).unsqueeze(0).to(self.device) 
        
        with torch.no_grad():
            outputs = self.model(image)
            _, predicted = torch.max(outputs, 1)
            return predicted.item() 
