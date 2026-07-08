name: social-post-generator
description: Generates platform-specific social media posts with hashtag suggestions and validates against character/hashtag limits

---

## Workflow: Social Media Post Creation

### Step-by-Step Instructions

1. **Capture requirements** - Ask for:
   - Target platform (twitter, linkedin, instagram)
   - Topic or key message
   - Desired tone (professional, casual, promotional)

2. **Draft the post** - Create content keeping platform character limits in mind

3. **Validate with script** - Run the validation script to check:
   - Character count vs platform limit
   - Hashtag count vs best practice range
   - URL detection for Twitter/X awareness

4. **Iterate if needed** - Adjust content based on validation results

5. **Present final post** - Show validated post with character/Hashtag status


### Output Template

**Draft Post:**
```
[PLATFORM]: [post content here]
```

**Validation Results:**
```
Platform: [platform]
Character count: [count]/[limit]
Hashtag count: [count] (recommended: [min]-[max])
[OK/WARNING] [status message]
```


### Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Script not found | Wrong path | Use `.claude/scripts/validate_post.py` |
| Character limit exceeded | Content too long | Trim text or split into thread |
| Hashtag count warning | Too many/few tags | Adjust to 1-2 (Twitter), 3-5 (LinkedIn), or 5-15 (Instagram) |
| URL detection missing | Non-standard URL format | Ensure URLs include http:// or https:// |
| Unicode error on Windows | Console encoding | Use ASCII characters (avoid ⚠️ ✓ emojis) |

"generate 3 post variants"