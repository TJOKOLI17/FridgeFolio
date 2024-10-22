package com.example.fridge;

import java.util.Optional;
import java.util.List;

import com.example.fridge.entity.Item;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ItemController {
    @Autowired
    private ItemRepository ItemRepository;

    @GetMapping
    public List<Item> findAllItems() {
        return ItemRepository.findAll();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Item> findItemById(@PathVariable(value = "id") long id) {
        Optional<Item> item;
        item = ItemRepository.findById(id);

        if(item.isPresent()) {
            return ResponseEntity.ok().body(item.get());
        } else {
            return ResponseEntity.notFound().build();
        }

    } 

     @PostMapping
    public Item saveItem(@Validated @RequestBody Item item) {

        return ItemRepository.save(item);
    }

    
}
